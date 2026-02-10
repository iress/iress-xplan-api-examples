#!/usr/bin/env bash
# This script is used to lint python code.
set -euo pipefail

echo "Format python code ..."
ruff format src "$@"
ruff check --fix src "$@"
