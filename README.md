# LLM Serving Characterization Lab

## Purpose

This project characterizes a single vLLM backend before adding routing, Kubernetes scheduling, llm-d, Kueue, prefill/decode disaggregation, or fleet-level operations.

The goal is not to prove that a model can run.

The goal is to understand how an LLM serving backend behaves as a queuing, batching, memory, and GPU-runtime system under controlled workload shapes.

This lab answers:

- What workload shapes increase Time To First Token?
- What workload shapes degrade decode smoothness?
- When does queueing begin before visible failure?
- How does prompt length affect prefill cost?
- How does output length affect decode residency?
- How does KV cache pressure affect safe concurrency?
- When does prefix reuse help?
- How does LoRA change serving behavior?
- What does it mean for a backend to be alive, ready, and safe to receive traffic?

This project is Build 1 in a larger AI infrastructure portfolio.

```text
Build 1: LLM Serving Characterization
        ↓
Build 2: Kubernetes Scheduling for GPU Inference Workloads
        ↓
Build 3: llm-d Routing Control Plane
        ↓
Build 4: Disaggregated Prefill/Decode Runtime
        ↓
Build 5: Inference Reliability, Observability, and Fleet Operations

```

## Scope of Build 1

Build 1 isolates a single vLLM backend to study its behavior as a queuing and GPU-runtime system. No routing, scheduling, or multi-backend orchestration is introduced yet. This ensures that all observed behaviors originate from the model, the runtime, and the GPU—not from distributed systems effects.

## Why This Build Exists

LLM serving is not normal HTTP serving.

A normal service is usually characterized by:

- request count
- payload size
- CPU
- database latency
- network latency

An LLM serving backend is shaped by:

- input sequence length
- output sequence length
- prefill cost
- decode loop behavior
- KV cache allocation
- batching policy
- queue depth
- GPU memory pressure
- prefix cache locality
- LoRA adapter residency
- request concurrency
- scheduler behavior inside the serving engine

A backend can look healthy while still delivering bad user experience.

For example:

- GPU utilization can look high while p99 latency is broken.
- Tokens/sec can look healthy while TTFT is unacceptable.
- Kubernetes readiness can pass while the backend is overloaded.
- The process can be alive while the model is not safe to receive new traffic.
- Average latency can look fine while short interactive requests suffer behind long-prefill requests.

This lab exists to make those failure modes visible.

## LLM-d Integration (Build 1.5)

LLM-d scenarios will be added to provide standardized measurements of:
- throughput scaling
- latency distributions
- KV-cache residency
- prefill/decode imbalance
- quantization effects (BF16, FP8, AWQ)

These experiments will be run on ACCESS GPU allocations (H100-class).

## Reproducibility

All experiments in this lab are:
- configuration-driven
- scriptable end-to-end
- parameterized by workload shape
- repeatable on local GPUs and ACCESS systems

Results, traces, and configurations will be published under `experiment-reports/`.


## Core Question

Before routing, scheduling, or operating anything:

Do we understand how one vLLM backend behaves under real workload shapes?

This project builds the evidence needed for later decisions about inference-aware routing, llm-d Endpoint Picker behavior, queue-aware load balancing, prefix-cache-aware routing, LoRA-adapter-aware routing, readiness semantics, admission control, SLO design, GPU capacity planning, observability, and incident response.

## System Boundary

In scope:

single vLLM backend
OpenAI-compatible API
controlled benchmark workloads
TTFT measurement
ITL / TPOT measurement
throughput measurement
vLLM metrics scraping
Prometheus
Grafana
startup log capture
KV cache observation
prefix reuse experiments
basic LoRA serving experiments
container runtime contract
readiness/liveness analysis

Out of scope:

llm-d EPP
multi-backend routing
Kueue
gang scheduling
Kubernetes autoscaling
prefill/decode disaggregation
multi-node GPU networking
RDMA
NCCL
production-grade MoE serving
large fleet operations

## Workload Taxonomy 

| Workload Class        | Prompt Tokens | Output Tokens | Main Stress                                   |
| --------------------- | ------------: | ------------: | --------------------------------------------- |
| Short interactive     |       128–512 |        64–256 | responsiveness and decode latency             |
| Long prefill          |        4k–16k |        64–256 | TTFT, prefill compute, KV allocation          |
| Long generation       |        512–2k |         1k–4k | decode residency and active sequence pressure |
| Mixed workload        |        varied |        varied | batching interference and tail latency        |
| Prefix reuse          | shared prefix |        varied | prefix cache locality                         |
| LoRA workload         |        varied |        varied | adapter loading, memory, and routing          |
| Burst traffic         |        varied |        varied | queue buildup and overload behavior           |
| Pathological workload |     very long |          long | failure boundaries and readiness semantics    |


## Key Metrics

### Request-level metrics:

- TTFT p50 / p95 / p99
- ITL or TPOT p50 / p95 / p99
- end-to-end latency
- request success rate
- request error rate
- timeout rate
- output tokens per second
- total tokens per second

## vLLM engine metrics:

- running requests
- waiting requests
- swapped requests
- prompt tokens processed
- generation tokens processed
- KV cache usage
- prefix cache hit rate if available
- preemptions
- LoRA-related request behavior if enabled

## System metrics:

- GPU utilization
- GPU memory used
- CPU utilization
- container memory
- network receive/transmit
- process restarts
- startup time
- model load time

## Experiment Plan

## First Experiment (Baseline)

- Model: Llama 3.1 8B Instruct (BF16)
- Engine: vLLM
- Workload: batch sweep (1, 8, 16, 32, 64)
- Sequence length: 2048
- Metrics: TTFT, decode TPS, GPU memory residency

## Experiment 001 — Single Backend

Question:

What is the baseline behavior of one vLLM backend under short, low-concurrency traffic?

## Experiment 002 — Prompt Length Pressure

Question:

How does increasing input sequence length affect TTFT and backend saturation?

Experiment 003 — Output Length Pressure

Question:

How does increasing output length affect decode residency and tail latency?

## Experiment 004 — Mixed Workload Interference

Question:

Do short interactive requests suffer when mixed with long-prefill or long-generation requests?

## Experiment 005 — Prefix Cache Locality

Question:

When does prefix reuse reduce prefill cost, and what would a router need to preserve that benefit?

## Experiment 006 — LoRA Serving Baseline

Question:

How does LoRA adapter serving differ operationally from base-model serving?

## Repository Layout 

```
llm-serving-characterization/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── workload-taxonomy.md
│   ├── benchmark-methodology.md
│   ├── vllm-triage-runbook.md
│   ├── startup-capacity-check.md
│   ├── promql-cheatsheet.md
│   ├── performance-remediation-tree.md
│   ├── capacity-model.md
│   ├── serving-pathologies.md
│   ├── container-contract.md
│   ├── wrong-vs-useful-benchmark.md
│   ├── build-1-review.md
│   └── experiment-reports/
├── workloads/
│   ├── short_prompts.jsonl
│   ├── long_prompts.jsonl
│   ├── mixed_prompts.jsonl
│   ├── prefix_reuse_prompts.jsonl
│   └── lora_prompts.jsonl
├── scripts/
│   ├── run_server.sh
│   ├── run_benchmark.py
│   ├── collect_metrics.sh
│   └── summarize_results.py
├── configs/
│   ├── prometheus.yml
│   └── docker-compose.yml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── servicemonitor.yaml
└── results/
    ├── raw/
    ├── summaries/
    └── graphs/

```

Results will be published in `experiment-reports/`.



