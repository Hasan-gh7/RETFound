#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" -B run_demo.py "$@"
