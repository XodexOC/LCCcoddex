#!/usr/bin/env bash
set -e

nasm -f elf64 solution.asm -o /tmp/lab.o
ld /tmp/lab.o -o /tmp/lab
/tmp/lab
