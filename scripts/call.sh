#!/usr/bin/env bash
# This script is used to run the commands.
set -euo pipefail

PYTHONPATH=$(pwd)/src python src/call.py "$@"