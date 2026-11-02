#!/bin/bash
set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <gcno-file> [gcno-file ...]" >&2
    exit 2
fi

GCOV_OUTPUT="$(LC_ALL=C gcov -n "$@" 2>&1)"
printf '%s\n' "${GCOV_OUTPUT}"

TOTAL="$({
    printf '%s\n' "${GCOV_OUTPUT}" |
        awk '
            /^Lines executed:/ {
                total = $0
            }
            END {
                if (total == "") {
                    exit 1
                }
                sub(/^Lines executed:/, "", total)
                sub(/ of .*$/, "", total)
                print total
            }
        '
})"

if [[ -z "${TOTAL}" ]]; then
    echo "ERROR: unable to extract total coverage from gcov output" >&2
    exit 1
fi

printf 'Total coverage:|%s\n' "${TOTAL}"
