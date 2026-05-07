# Experiment 001A — CPU Real-Model Baseline

## Question

Can the benchmark harness measure real model execution latency, first-token latency, inter-token latency, token counts, and memory usage on a CPU-only machine?

## Why This Exists

This is not a vLLM performance benchmark.

This experiment validates the local measurement workflow before paid GPU time is used. The goal is to prove that the benchmark harness can run a real model, tokenize real prompts, generate real tokens, measure TTFT, estimate ITL, capture end-to-end latency, and write raw plus summary results.

## Backend

Transformers + PyTorch CPU

## Model

`sshleifer/tiny-gpt2`

## Workload

`workloads/short_prompts.jsonl`

## Run Configuration

| Field | Value |
|---|---:|
| Requests | 5 |
| Max new tokens | 32 |
| Average input tokens | 12.2 |
| Average output tokens | 32 |

## Results

| Metric | Value |
|---|---:|
| Successes | 5 / 5 |
| TTFT p50 | 0.00365 s |
| TTFT p95 | 0.00438 s |
| ITL p50 | 0.00315 s |
| ITL p95 | 0.00528 s |
| E2E latency p50 | 0.10110 s |
| E2E latency p95 | 0.16817 s |
| Average tokens/sec | 289.11 |
| Max RSS memory | 374.58 MB |

## Raw Summary

```json
{
  "requests": 5,
  "successes": 5,
  "ttft_p50_s": 0.0036497150003924617,
  "ttft_p95_s": 0.004381381199891621,
  "itl_p50_s": 0.003152325290307823,
  "itl_p95_s": 0.005283899399998312,
  "e2e_p50_s": 0.10110070500013535,
  "e2e_p95_s": 0.16817317400000317,
  "tokens_per_second_avg": 289.1072721741732,
  "input_tokens_avg": 12.2,
  "output_tokens_avg": 32,
  "rss_after_mb_max": 374.58203125,
  "model": "sshleifer/tiny-gpt2",
  "workload": "workloads/short_prompts.jsonl",
  "max_new_tokens_cap": 32
}