cat > docs/experiment-reports/001-baseline.md <<'EOF'
# Experiment 001 — Local vLLM Baseline

## Question

Can one local vLLM backend serve a controlled short-prompt workload while exposing enough metrics to measure TTFT, ITL/TPOT, throughput, queue depth, and GPU memory?

## Why This Experiment Exists

This is the first real vLLM serving baseline for Build #1.

The purpose is not to maximize throughput. The purpose is to establish a stable measurement loop:

```text
vLLM backend
→ controlled workload
→ streaming benchmark
→ TTFT / ITL / E2E latency
→ /metrics scrape
→ GPU memory snapshot
→ written interpretation


This baseline becomes the reference point for prompt-length pressure, output-length pressure, mixed workload interference, prefix-cache behavior, and LoRA serving behavior.

Setup
Field	Value
Model	
vLLM version	
CUDA version	
GPU	
GPU memory	
Driver version	
Workload	workloads/baseline_short.jsonl
Max output tokens	64
Server command	scripts/run_server.sh
Benchmark command	scripts/run_benchmark.sh
Server Configuration
Setting	Value
--gpu-memory-utilization	
--max-model-len	
--served-model-name	baseline-model
Host / port	0.0.0.0:8000
Request-Level Results
Metric	Value
Requests	
Successes	
TTFT p50	
TTFT p95	
ITL / TPOT p50	
ITL / TPOT p95	
E2E latency p50	
E2E latency p95	
Throughput avg tokens/sec	
vLLM Engine Metrics
Metric	Value / Observation
vllm:num_requests_running	
vllm:num_requests_waiting	
vllm:num_requests_swapped	
vllm:kv_cache_usage_perc	
Prompt token metrics	
Generation token metrics	
GPU Snapshot
Metric	Value
GPU name	
GPU memory total	
GPU memory used after model load	
GPU utilization during run	
Power draw	
Startup Log Observations

Capture from results/raw/baseline/startup/:

model load time:
memory allocation:
KV cache allocation:
warnings:
max model length:
CUDA graph / compilation notes if present:
Observations
Interpretation
What This Informs Later

This baseline defines the stable reference point for the rest of Build #1.

It tells us:

whether the backend is healthy under a simple workload
what normal TTFT looks like before pressure tests
what normal ITL/TPOT looks like before pressure tests
how much GPU memory is consumed at startup
whether queue depth appears under light load
which vLLM metrics are available in this version
Limitations

This experiment does not test saturation, long prompts, long generations, mixed workloads, prefix cache behavior, LoRA, or multi-backend routing.