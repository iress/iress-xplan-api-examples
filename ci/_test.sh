#!/usr/bin/env bash
set -euo pipefail

echo "Running Unit Tests and Coverage"

pytest .
coverage report
