# Experiment 002 — Prompt Length Pressure

## Question

How does increasing prompt length affect TTFT and backend saturation?

## Hypothesis

Longer prompts increase prefill cost and KV allocation pressure, so TTFT should rise even when output length remains fixed.

## Result Summary

## Saturation Point

## Interpretation

## Design Implication

Long prompts should not necessarily be routed the same way as short interactive requests.
Future routing layers may need workload classification or admission controls.