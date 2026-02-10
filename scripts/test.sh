#!/usr/bin/env bash
# This script is used to test python code.
set -euo pipefail

PYTHONPATH=src python -m pytest -vvv --cov-config=.coveragerc --cov-report xml:output/coverage.xml --cov=. src/
