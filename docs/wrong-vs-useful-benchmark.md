# Wrong vs Useful Benchmark

## Wrong Benchmark

“I sent 100 requests and achieved 70 tokens/sec.”

This is incomplete because it does not describe workload shape, concurrency, prompt length, output length, tail latency, queue depth, or failure mode.

## Useful Benchmark

“Under a 70/20/10 mixed workload, average throughput remained stable, but p95 TTFT crossed 2 seconds at concurrency 16. The waiting queue began to grow before GPU utilization reached 100%. This suggests the backend was limited by scheduling and prefill interference, not raw GPU saturation.”

## Why This Matters

A scheduler using only throughput or GPU utilization would make the wrong decision.
A better scheduler needs request-shape awareness, queue-depth signals, and overload protection.