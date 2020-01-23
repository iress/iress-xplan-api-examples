#!/usr/bin/env bash
# This task validates the Terraform code, compiles the application into a runtime docker image. Does not require credentials or any other pre-requisites
set -euo pipefail

docker build -t iress/xplan-api-examples .

docker run iress/xplan-api-examples
