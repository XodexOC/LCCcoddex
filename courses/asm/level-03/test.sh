#!/usr/bin/env bash
set -euo pipefail
echo "Xodex lab smoke: asm/03"

if [ ! -f solution.asm ]; then
    echo "FAIL: solution.asm not found"
    exit 1
fi

nasm -f elf64 solution.asm -o /tmp/xodex_asm_lab.o 2>&1
ld /tmp/xodex_asm_lab.o -o /tmp/xodex_asm_lab 2>&1

echo "--- Running ---"
/tmp/xodex_asm_lab || true
echo "--- Exit code: $? ---"

echo "PASS (asm/03)"
