#!/usr/bin/env python3
import sys

current = None
count = 0

for line in sys.stdin:
    player, val = line.strip().split('\t')
    val = int(val)
    if player == current:
        count += val
    else:
        if current:
            print(f"{current}\t{count}")
        current = player
        count = val

if current:
    print(f"{current}\t{count}")
