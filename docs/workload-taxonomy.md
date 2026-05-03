# Workload Taxonomy

## Why workload shape matters

LLM serving performance is not determined by request count alone.

Two workloads with the same request rate can behave very differently depending on prompt tokens, output tokens, prefix reuse, and adapter usage.

## Workload Classes

| Class | Prompt Tokens | Output Tokens | Main Stress |
|---|---:|---:|---|
| Short interactive | 128–512 | 64–256 | decode responsiveness |
| Long prefill | 4k–16k | 64–256 | TTFT and KV allocation |
| Long generation | 512–2k | 1k–4k | decode residency |
| Mixed workload | varied | varied | batching interference |
| Prefix reuse | shared prefix | varied | cache locality |
| LoRA workload | varied | varied | adapter loading and memory |
| Burst traffic | varied | varied | queue buildup |