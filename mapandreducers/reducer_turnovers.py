#!/usr/bin/env python3
import sys
from collections import Counter

counts = Counter()
for line in sys.stdin:
    team, val = line.strip().split('\t')
    counts[team] += int(val)

for team, c in counts.items():
    print(f"{team}\t{c}")
