#!/usr/bin/env bash
# This task runs unit tests and coverage
set -euo pipefail

docker build -t iress/xplan-api-examples .

docker run --user root:root iress/xplan-api-examples ./ci/_test.sh
