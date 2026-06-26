#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../framework/backend"
uvicorn agentops_mesh_api.main:app --reload
