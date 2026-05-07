#!/usr/bin/env bash
set -euo pipefail

VLLM_URL="${VLLM_URL:-http://localhost:8000}"
OUT_DIR="${OUT_DIR:-results/raw/baseline/metrics}"
TS="$(date +%Y%m%d-%H%M%S)"

mkdir -p "${OUT_DIR}"

echo "Collecting vLLM metrics..."
curl -s "${VLLM_URL}/metrics" > "${OUT_DIR}/vllm-metrics-${TS}.txt"

echo "Collecting GPU snapshot..."
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi > "${OUT_DIR}/nvidia-smi-${TS}.txt"
  nvidia-smi --query-gpu=timestamp,name,index,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free,power.draw,temperature.gpu \
    --format=csv > "${OUT_DIR}/nvidia-smi-query-${TS}.csv"
else
  echo "nvidia-smi not found" > "${OUT_DIR}/nvidia-smi-${TS}.txt"
fi

echo "Wrote metrics to ${OUT_DIR}"
