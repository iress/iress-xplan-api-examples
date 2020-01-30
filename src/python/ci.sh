#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]
then
    TASK="help"
else
    TASK=$1
fi

[[ ${TASK} =~ [^[:alnum:]_-] ]] && { echo "bad param" >&2; exit 1; }
"$(dirname "$(readlink "$0")")/ci/${TASK}.sh"
