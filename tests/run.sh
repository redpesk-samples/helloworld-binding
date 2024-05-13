#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TEST_BINDING_PATH=${SCRIPT_DIR}/../build python ${SCRIPT_DIR}/tests.py --tap
