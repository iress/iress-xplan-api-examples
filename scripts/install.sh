#!/usr/bin/env bash
# This script is used to install python dependencies.
set -euo pipefail

echo "Installing python dependencies..."
uv sync "$@"
