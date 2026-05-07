#!/usr/bin/env python3

import argparse
import json
import statistics
import time
from pathlib import Path

import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def percentile(values, p):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * (p / 100)
    f = int(k)
    c = min(f + 1, len(values) - 1)
    if f == c:
        return values[int(k)]
    return values[f] * (c - k) + values[c] * (k - f)


def load_prompts(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def run_one(model, tokenizer, prompt, max_new_tokens):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    input_tokens = int(input_ids.shape[-1])
    generated_token_ids = []

    process = psutil.Process()
    rss_before = process.memory_info().rss

    start = time.perf_counter()
    first_token_time = None

    current_ids = input_ids

    with torch.inference_mode():
        for _ in range(max_new_tokens):
            outputs = model(current_ids)
            next_token_logits = outputs.logits[:, -1, :]
            next_token_id = torch.argmax(next_token_logits, dim=-1, keepdim=True)

            now = time.perf_counter()
            if first_token_time is None:
                first_token_time = now

            generated_token_ids.append(int(next_token_id.item()))
            current_ids = torch.cat([current_ids, next_token_id], dim=-1)

            if tokenizer.eos_token_id is not None and int(next_token_id.item()) == tokenizer.eos_token_id:
                break

    end = time.perf_counter()
    rss_after = process.memory_info().rss

    output_tokens = len(generated_token_ids)
    ttft_s = (first_token_time - start) if first_token_time else None
    e2e_s = end - start

    if output_tokens > 1 and ttft_s is not None:
        decode_time_s = e2e_s - ttft_s
        itl_s = decode_time_s / max(output_tokens - 1, 1)
    else:
        itl_s = None

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "ttft_s": ttft_s,
        "itl_s": itl_s,
        "e2e_latency_s": e2e_s,
        "tokens_per_second": output_tokens / e2e_s if e2e_s > 0 else None,
        "rss_before_mb": rss_before / (1024 * 1024),
        "rss_after_mb": rss_after / (1024 * 1024),
        "rss_delta_mb": (rss_after - rss_before) / (1024 * 1024),
    }


def summarize(results):
    def col(name):
        return [r[name] for r in results if r.get(name) is not None]

    summary = {
        "requests": len(results),
        "successes": len(results),
        "ttft_p50_s": percentile(col("ttft_s"), 50),
        "ttft_p95_s": percentile(col("ttft_s"), 95),
        "itl_p50_s": percentile(col("itl_s"), 50),
        "itl_p95_s": percentile(col("itl_s"), 95),
        "e2e_p50_s": percentile(col("e2e_latency_s"), 50),
        "e2e_p95_s": percentile(col("e2e_latency_s"), 95),
        "tokens_per_second_avg": statistics.mean(col("tokens_per_second")) if col("tokens_per_second") else None,
        "input_tokens_avg": statistics.mean(col("input_tokens")) if col("input_tokens") else None,
        "output_tokens_avg": statistics.mean(col("output_tokens")) if col("output_tokens") else None,
        "rss_after_mb_max": max(col("rss_after_mb")) if col("rss_after_mb") else None,
    }
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="sshleifer/tiny-gpt2")
    parser.add_argument("--workload", default="workloads/short_prompts.jsonl")
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--out-dir", default="results/raw/cpu")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    run_id = time.strftime("%Y%m%d-%H%M%S")
    raw_path = out_dir / f"cpu-real-inference-{run_id}.jsonl"
    summary_path = Path("results/summaries") / f"cpu-real-inference-summary-{run_id}.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading tokenizer: {args.model}")
    tokenizer = AutoTokenizer.from_pretrained(args.model)

    print(f"Loading model: {args.model}")
    model = AutoModelForCausalLM.from_pretrained(args.model)
    model.eval()

    prompts = load_prompts(args.workload)
    results = []

    print(f"Running {len(prompts)} prompts")
    for row in prompts:
        prompt = row["prompt"]
        max_tokens = int(row.get("max_tokens", args.max_new_tokens))
        max_tokens = min(max_tokens, args.max_new_tokens)

        started = time.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            metrics = run_one(model, tokenizer, prompt, max_tokens)
            record = {
                "id": row.get("id"),
                "model": args.model,
                "started_at": started,
                "prompt_chars": len(prompt),
                **metrics,
                "status": "ok",
            }
        except Exception as e:
            record = {
                "id": row.get("id"),
                "model": args.model,
                "started_at": started,
                "status": "error",
                "error": str(e),
            }

        results.append(record)
        with open(raw_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        print(json.dumps(record, indent=2))

    ok_results = [r for r in results if r.get("status") == "ok"]
    summary = summarize(ok_results)
    summary["model"] = args.model
    summary["workload"] = args.workload
    summary["max_new_tokens_cap"] = args.max_new_tokens

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nSummary:")
    print(json.dumps(summary, indent=2))
    print(f"\nRaw results: {raw_path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
