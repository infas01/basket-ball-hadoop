#!/usr/bin/env python3
import sys, csv

# Skip the first title line
_ = next(sys.stdin)

reader = csv.DictReader(sys.stdin)
for row in reader:
    desc = ((row.get('HOMEDESCRIPTION') or '') + (row.get('VISITORDESCRIPTION') or '')).upper()
    if 'FOUL' in desc:
        player = row.get('PLAYER1_NAME') or 'UNKNOWN'
        print(f"{player}\t1")
