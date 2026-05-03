# Capacity Model

## Purpose

This document estimates the safe operating envelope of one vLLM backend under different workload shapes.

## Definitions

- Safe concurrency:
- TTFT SLO:
- ITL/TPOT SLO:
- Max acceptable queue depth:
- Max GPU memory threshold:
- Error budget:

## Findings

| Workload | Safe Concurrency | First Breaking Signal | Notes |
|---|---:|---|---|
| short interactive | | | |
| long prompt | | | |
| long generation | | | |
| mixed | | | |
| prefix reuse | | | |
| LoRA | | | |

## Design Implications

- Long-prefill traffic should be classified separately.
- Queue depth is a better early overload signal than process health.
- Prefix locality may be worth preserving in routing.
- Adapter-aware routing should be considered for LoRA-heavy tenants.