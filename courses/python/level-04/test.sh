#!/usr/bin/env bash
set -euo pipefail
echo "Xodex lab smoke: python/04"
command -v python3 >/dev/null && echo OK_python3
if [ -f solution.c ]; then gcc -Wall -Wextra -o /tmp/xodex_lab_sol solution.c && /tmp/xodex_lab_sol; fi
if [ -f solution.py ]; then python3 solution.py; fi
if [ -f solution.rs ]; then rustc -O solution.rs -o /tmp/xodex_lab_rs && /tmp/xodex_lab_rs; fi
if [ -f solution.sql ]; then sqlite3 :memory: < solution.sql; fi
if [ -f solution.sh ]; then bash solution.sh; fi
echo "PASS (smoke)"
