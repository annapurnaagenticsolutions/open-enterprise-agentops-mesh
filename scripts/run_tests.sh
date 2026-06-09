#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../framework/backend"
pytest
