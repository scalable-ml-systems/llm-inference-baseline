# Benchmark Methodology

## Purpose

This benchmark does not seek a single maximum throughput number.
It seeks to identify how serving behavior changes under different workload shapes.

## Metrics

- TTFT p50/p95/p99
- ITL or TPOT p50/p95/p99
- End-to-end latency
- Requests/sec
- Tokens/sec
- Running requests
- Waiting requests
- KV cache usage
- GPU memory
- Error rate
- Timeout rate

## Run Metadata

Each run must record:

- model name
- model revision
- vLLM version
- CUDA version
- GPU type
- GPU memory
- container image
- command-line flags
- workload file
- concurrency
- request rate
- max output tokens
- warmup duration
- measurement duration