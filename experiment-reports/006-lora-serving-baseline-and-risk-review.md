# Experiment 006 — LoRA Serving Baseline and Risk Review

## Question

How does LoRA adapter serving differ operationally from base-model serving?

## What I Tested

- base model only
- single adapter
- multiple adapters
- adapter switching

## Observations

## Operational Risks

- adapter cold load
- memory pressure
- adapter routing
- tenant isolation
- unsafe dynamic loading
- version mismatch

## Future Design Implication

A future router should be adapter-aware. It should avoid sending adapter-specific traffic to backends where the adapter is cold or unavailable unless the latency tradeoff is acceptable.