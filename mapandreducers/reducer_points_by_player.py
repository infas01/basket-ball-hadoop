#!/usr/bin/env python3
import sys
from collections import defaultdict

totals = defaultdict(int)
for line in sys.stdin:
    player, pts = line.strip().split('\t')
    totals[player] += int(pts)

for player, pts in totals.items():
    print(f"{player}\t{pts}")
