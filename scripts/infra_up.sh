#!/usr/bin/env bash
set -euo pipefail

docker compose -f configs/docker-compose.yml up -d

echo ""
echo "Prometheus: http://localhost:9090"
echo "Grafana:    http://localhost:3000"
echo "Grafana login: admin / admin"
