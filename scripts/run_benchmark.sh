#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000/v1}"
MODEL="${MODEL:-baseline-model}"
WORKLOAD="${WORKLOAD:-workloads/baseline_short.jsonl}"

python scripts/run_benchmark.py \
  --base-url "${BASE_URL}" \
  --model "${MODEL}" \
  --workload "${WORKLOAD}"
