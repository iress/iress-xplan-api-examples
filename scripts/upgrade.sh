#!/usr/bin/env bash
# This script is used to Upgrade app dependencies.
set -euo pipefail

echo "Upgrade Python dependencies ..."
uv sync --all-groups --upgrade "$@"
