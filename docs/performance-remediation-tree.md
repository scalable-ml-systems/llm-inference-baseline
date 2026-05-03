Symptom: High TTFT
  ├── num_requests_waiting > 0?
  │     ├── yes → server saturated / queueing
  │     │          actions: add replica, reduce max_num_seqs, admission control
  │     └── no → likely long prefill / prompt length issue
  │                actions: inspect ISL, use prefix caching, chunked prefill tuning
  │
Symptom: High ITL
  ├── high concurrency?
  │     ├── yes → decode batch pressure
  │     └── no → hardware bandwidth / model size / TP overhead
  │
Symptom: Waiting queue grows
  ├── KV cache near 100%?
  │     ├── yes → memory pressure
  │     └── no → other scheduler/resource bottleneck