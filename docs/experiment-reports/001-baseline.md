# Experiment 001 — Baseline Single Backend

## Question

What is the baseline behavior of one vLLM backend under short, low-concurrency traffic?

## Why This Experiment Exists

This establishes the clean reference point for all later experiments.

Without a baseline, prompt-length pressure, output-length pressure, prefix reuse behavior, and LoRA overhead cannot be interpreted clearly.

## Setup

| Field | Value |
|---|---|
| Model | |
| vLLM version | |
| CUDA version | |
| GPU | |
| GPU memory | |
| Workload | short_prompts.jsonl |
| Concurrency | |
| Max output tokens | |
| Measurement duration | |
| vLLM flags | |

## Results

| Metric | Value |
|---|---:|
| Request count | |
| Success rate | |
| p50 latency | |
| p95 latency | |
| p99 latency | |
| TTFT p50 | |
| TTFT p95 | |
| ITL / TPOT p95 | |
| Tokens/sec | |
| Running requests | |
| Waiting requests | |
| KV cache usage | |
| GPU memory used | |

## Startup Observations

Capture relevant startup log details:

- model load time:
- GPU memory available:
- KV cache allocation:
- max concurrency estimate:
- warnings:

## Observations

## Interpretation

## What This Informs Later

This baseline gives us a clean comparison point for later prompt-length, output-length, prefix-cache, mixed-workload, and LoRA experiments.

## Limitations

This experiment does not prove behavior under mixed workloads, long contexts, high concurrency, LoRA, or multi-backend routing.
