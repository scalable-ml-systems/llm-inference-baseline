Context: Derived from hands-on characterization of vLLM serving under realistic workloads (prompt length, concurrency, LoRA, prefix caching). This document defines operational rules for backend health, distinguishing Kubernetes probes from fine-grained traffic admission needed for llm-d EPP routing and capacity planning.

Why Admission Rules Matter
Standard K8s liveness/readiness (/health, /v1/models) confirm "server alive + model loaded," but fail inference serving:

Pod ready → still OOMs on KV pressure

Traffic routed → TTFT explodes from queue saturation

Adapter cold → 800ms penalty per switch

These rules use vLLM /metrics (Prometheus): kv_cache_usage_perc, num_requests_running/waiting, num_preemptions_total for traffic-ready decisions beyond probes.

1. Readiness/Liveness Decision Table
Coarse K8s gates + nuanced "traffic-ready" for routing.

| Condition                       | Liveness | Readiness | Traffic-Ready | Why                      |
| ------------------------------- | -------- | --------- | ------------- | ------------------------ |
| Process running, model unloaded | ✅        | ❌         | ❌             | Cannot serve llm-d       |
| Model loaded, queue empty       | ✅        | ✅         | ✅             | Optimal                  |
| Model loaded, queue >5          | ✅        | ✅         | ⚠️            | Saturated; monitor       |
| GPU mem >90% / KV >85%          | ✅        | ⚠️        | ❌             | OOM/preemption risk vllm |
| Draining/shutdown               | ✅        | ❌         | ❌             | No new traffic           |
| Adapter missing/non-resident    | ✅        | ✅         | Adapter=❌     | Base OK, LoRA risky vllm |

Probes Config (llm-d style):
startupProbe:
  httpGet: { path: /v1/models, port: 8000 }
  failureThreshold: 60  # 30min model load
readinessProbe:
  httpGet: { path: /v1/models, port: 8000 }
livenessProbe:
  httpGet: { path: /health, port: 8000 }

2. Serving Pathologies Catalog
Symptom → signal → mitigation. Guides overload prediction and routing policy.
| Pathology           | Symptom            | Root Cause           | Detection Signals vllm         | Mitigation (Builds 2–5)       |
| ------------------- | ------------------ | -------------------- | ------------------------------ | ----------------------------- |
| TTFT Cliff          | p95 TTFT >2s       | Long prefill + queue | TTFT + num_requests_waiting >0 | Workload classifier → route   |
| Tail Latency        | p99 bad, avg OK    | Interference         | p95/p99 ITL                    | Prefix/LoRA-aware EPP (Lab 3) |
| Alive but Unsafe    | Health ✅, timeouts | Shallow probes       | queue_depth >3, KV>85%         | Traffic admission rules       |
| Prefix Miss Storm   | Repeated slow      | No locality          | prefix_cache_hit_rate <70%     | Sticky routing (Lab 3)        |
| Adapter Cold Path   | First LoRA 800ms   | Non-resident         | Adapter load latency           | Residency scoring (Lab 3)     |
| Retry Amplification | Overload worsens   | Gateway retries      | Retry count + queue            | Backpressure (Lab 3)          |
| KV Pressure         | Mem →100%          | Long contexts        | kv_cache_usage_perc, GPU mem   | Admission control (Lab 2)     |





