#!/usr/bin/env bash
set -euo pipefail

echo "Installing dependencies..."
devbox run install

echo "Linting code..."
devbox run lint

echo "Running Unit Tests and Coverage..."
devbox run test
