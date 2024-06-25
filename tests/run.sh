#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LD_LIBRARY_PATH=${SCRIPT_DIR}/../build python ${SCRIPT_DIR}/tests.py
