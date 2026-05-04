#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-Qwen/Qwen2.5-1.5B-Instruct}"
PORT="${PORT:-8000}"
SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-baseline-model}"

mkdir -p results/raw/startup

echo "Starting vLLM server"
echo "Model: ${MODEL}"
echo "Port: ${PORT}"
echo "Served model name: ${SERVED_MODEL_NAME}"

python -m vllm.entrypoints.openai.api_server \
  --model "${MODEL}" \
  --served-model-name "${SERVED_MODEL_NAME}" \
  --host 0.0.0.0 \
  --port "${PORT}" \
  2>&1 | tee "results/raw/startup/vllm-startup-$(date +%Y%m%d-%H%M%S).log"
