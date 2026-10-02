#!/usr/bin/env bash
set -euo pipefail

APEX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 não foi encontrado. Instale em https://www.python.org/downloads/ e tente novamente."
  exit 1
fi

exec python3 "$APEX_ROOT/servidor.py" "$@"
