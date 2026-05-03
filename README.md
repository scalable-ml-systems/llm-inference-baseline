# LLM Serving Baseline Lab:  Test Harness for the rest of the builds. 

This project characterizes a single vLLM backend under realistic workload shapes before adding routing, scheduling, or multi-backend orchestration.

The goal is to understand how prompt length, output length, concurrency, batching, KV cache behavior, prefix reuse, and LoRA adapters affect TTFT, ITL/TPOT, throughput, queue depth, GPU memory pressure, and backend readiness.

This lab produces artifacts used by later builds:
- Kubernetes GPU scheduling
- llm-d / EPP routing
- prefill/decode disaggregation
- reliability and observability engineering


# define what it means for a backend to be ready for traffic. 
