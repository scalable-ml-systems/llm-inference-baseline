## Key Observation

### Model : distilgpt2 

The first request behaved differently from later requests.

The first request had:

- TTFT: 151 ms
- E2E latency: 2.09 s
- RSS memory increase: 354 MB

Later requests had:

- TTFT around 60–70 ms
- E2E latency around 1.92–1.98 s
- minimal additional RSS growth

## Raw Summary

``` Json
{
  "requests": 5,
  "successes": 5,
  "ttft_p50_s": 0.07005397700004323,
  "ttft_p95_s": 0.13535654360002808,
  "itl_p50_s": 0.06136433880645552,
  "itl_p95_s": 0.06243386988387483,
  "e2e_p50_s": 1.9740064010002243,
  "e2e_p95_s": 2.0704749258001356,
  "tokens_per_second_avg": 16.14395821247228,
  "input_tokens_avg": 12.2,
  "output_tokens_avg": 32,
  "rss_after_mb_max": 753.28515625,
  "model": "distilgpt2",
  "workload": "workloads/short_prompts.jsonl",
  "max_new_tokens_cap": 32
}

This suggests the first request paid warmup and memory allocation cost. Future experiments should separate cold-start behavior from steady-state behavior.