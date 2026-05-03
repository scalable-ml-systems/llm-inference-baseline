| Pathology | Symptom | Root Cause | Detection | Mitigation |
|-----------|---------|------------|-----------|------------|
| TTFT Cliff | p95 >2s | Long prefill + queue | TTFT + `num_waiting` | Long-prompt classifier |
| Tail Latency | p99 bad, avg OK | Workload interference | p95/p99 ITL | Prefix-aware routing |
| Alive-Unsafe | Health ✅, users timeout | Shallow probes | Queue>3, KV>85% | Traffic admission |
| Prefix Miss Storm | Repeated prompts slow | No locality | Cache hit <70% | Sticky routing |
| Adapter Cold | First LoRA req 800ms | Non-resident | Adapter load time | Residency-aware EPP |
| Retry Storm | Overload worsens | Gateway retries | Retry count + queue | Backpressure signals |
| KV Pressure | Mem →100% | Long contexts | `kv_cache_usage_perc` | Admission control |