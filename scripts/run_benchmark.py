#!/usr/bin/env python3

import argparse
import csv
import json
import statistics
import time
from pathlib import Path

import requests


def percentile(values, p):
    values = [v for v in values if v is not None]
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * (p / 100)
    f = int(k)
    c = min(f + 1, len(values) - 1)
    if f == c:
        return values[f]
    return values[f] * (c - k) + values[c] * (k - f)


def load_workload(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def estimate_itl(e2e_s, ttft_s, output_tokens):
    if ttft_s is None or output_tokens <= 1:
        return None
    return (e2e_s - ttft_s) / max(output_tokens - 1, 1)


def run_one(base_url, model, row, timeout_s):
    url = f"{base_url.rstrip('/')}/chat/completions"

    payload = {
        "model": model,
        "messages": row["messages"],
        "max_tokens": int(row.get("max_tokens", 64)),
        "temperature": float(row.get("temperature", 0.0)),
        "stream": True,
    }

    start = time.perf_counter()
    first_token_time = None
    chunks = []
    output_text_parts = []

    with requests.post(url, json=payload, stream=True, timeout=timeout_s) as resp:
        resp.raise_for_status()

        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue

            line = raw_line.strip()
            if not line.startswith("data:"):
                continue

            data = line[len("data:"):].strip()

            if data == "[DONE]":
                break

            now = time.perf_counter()
            if first_token_time is None:
                first_token_time = now

            try:
                event = json.loads(data)
            except json.JSONDecodeError:
                continue

            chunks.append(event)

            choices = event.get("choices", [])
            if choices:
                delta = choices[0].get("delta", {})
                content = delta.get("content")
                if content:
                    output_text_parts.append(content)

    end = time.perf_counter()

    output_text = "".join(output_text_parts)
    # This is approximate. The real token count should later be replaced with tokenizer-based counting.
    approx_output_tokens = max(1, len(output_text.split()))

    ttft_s = (first_token_time - start) if first_token_time else None
    e2e_s = end - start
    itl_s = estimate_itl(e2e_s, ttft_s, approx_output_tokens)

    return {
        "id": row.get("id"),
        "status": "ok",
        "ttft_s": ttft_s,
        "itl_s": itl_s,
        "e2e_latency_s": e2e_s,
        "approx_output_tokens": approx_output_tokens,
        "approx_tokens_per_second": approx_output_tokens / e2e_s if e2e_s > 0 else None,
        "chunks": len(chunks),
    }


def summarize(records):
    ok = [r for r in records if r.get("status") == "ok"]

    def col(name):
        return [r.get(name) for r in ok if r.get(name) is not None]

    return {
        "requests": len(records),
        "successes": len(ok),
        "ttft_p50_s": percentile(col("ttft_s"), 50),
        "ttft_p95_s": percentile(col("ttft_s"), 95),
        "itl_p50_s": percentile(col("itl_s"), 50),
        "itl_p95_s": percentile(col("itl_s"), 95),
        "e2e_p50_s": percentile(col("e2e_latency_s"), 50),
        "e2e_p95_s": percentile(col("e2e_latency_s"), 95),
        "tokens_per_second_avg": statistics.mean(col("approx_tokens_per_second")) if col("approx_tokens_per_second") else None,
        "output_tokens_avg_approx": statistics.mean(col("approx_output_tokens")) if col("approx_output_tokens") else None,
    }


def write_csv(path, summary):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for k, v in summary.items():
            writer.writerow([k, v])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000/v1")
    parser.add_argument("--model", default="baseline-model")
    parser.add_argument("--workload", default="workloads/baseline_short.jsonl")
    parser.add_argument("--out-dir", default="results/raw/baseline")
    parser.add_argument("--summary-dir", default="results/summaries")
    parser.add_argument("--timeout-s", type=int, default=120)
    args = parser.parse_args()

    ts = time.strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out_dir)
    summary_dir = Path(args.summary_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    raw_path = out_dir / f"baseline-requests-{ts}.jsonl"
    summary_json_path = summary_dir / f"001-baseline-summary-{ts}.json"
    summary_csv_path = summary_dir / f"001-baseline-summary-{ts}.csv"

    workload = load_workload(args.workload)
    records = []

    for row in workload:
        try:
            record = run_one(args.base_url, args.model, row, args.timeout_s)
        except Exception as e:
            record = {
                "id": row.get("id"),
                "status": "error",
                "error": str(e),
            }

        records.append(record)
        print(json.dumps(record, indent=2))

        with open(raw_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    summary = summarize(records)
    summary["model"] = args.model
    summary["workload"] = args.workload
    summary["base_url"] = args.base_url

    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    write_csv(summary_csv_path, summary)

    print("\nSummary:")
    print(json.dumps(summary, indent=2))
    print(f"\nRaw results: {raw_path}")
    print(f"Summary JSON: {summary_json_path}")
    print(f"Summary CSV: {summary_csv_path}")


if __name__ == "__main__":
    main()
