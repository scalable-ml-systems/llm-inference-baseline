#!/usr/bin/env bash
set -euo pipefail

VLLM_URL="${VLLM_URL:-http://localhost:8000}"
OUT_DIR="${OUT_DIR:-results/raw/metrics}"
TS="$(date +%Y%m%d-%H%M%S)"

mkdir -p "${OUT_DIR}"

echo "Collecting vLLM metrics from ${VLLM_URL}/metrics"

curl -s "${VLLM_URL}/metrics" > "${OUT_DIR}/vllm-metrics-${TS}.txt"

echo "Wrote ${OUT_DIR}/vllm-metrics-${TS}.txt"
