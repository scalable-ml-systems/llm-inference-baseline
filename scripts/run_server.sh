#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-Qwen/Qwen3-0.6B}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-baseline-model}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.85}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-4096}"

mkdir -p results/raw/baseline/startup

TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="results/raw/baseline/startup/vllm-startup-${TS}.log"

echo "Starting vLLM baseline server"
echo "Model: ${MODEL}"
echo "Host: ${HOST}"
echo "Port: ${PORT}"
echo "Served model name: ${SERVED_MODEL_NAME}"
echo "GPU memory utilization: ${GPU_MEMORY_UTILIZATION}"
echo "Max model length: ${MAX_MODEL_LEN}"
echo "Startup log: ${LOG_FILE}"

vllm serve "${MODEL}" \
  --host "${HOST}" \
  --port "${PORT}" \
  --served-model-name "${SERVED_MODEL_NAME}" \
  --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION}" \
  --max-model-len "${MAX_MODEL_LEN}" \
  2>&1 | tee "${LOG_FILE}"
