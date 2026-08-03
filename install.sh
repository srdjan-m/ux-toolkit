#!/usr/bin/env bash
# Thin wrapper around install.py for macOS/Linux, where `python` often isn't on PATH.
# All arguments are passed straight through:
#
#   ./install.sh                          # dry run
#   ./install.sh --apply --profile personal
#
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        exec "$candidate" "$here/install.py" "$@"
    fi
done

echo "error: no python3 or python found on PATH — install Python 3.9+ first." >&2
exit 1
