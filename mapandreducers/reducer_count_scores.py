#!/usr/bin/env python3
import sys

total = 0
for line in sys.stdin:
    _, cnt = line.strip().split('\t')
    total += int(cnt)
print(f"TotalScoringEvents\t{total}")
