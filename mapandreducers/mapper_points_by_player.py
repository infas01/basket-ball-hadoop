#!/usr/bin/env python3
import sys, csv, re

# Skip the first title line
_ = next(sys.stdin)

reader = csv.DictReader(sys.stdin)
for row in reader:
    desc = ((row.get('HOMEDESCRIPTION') or '') + (row.get('VISITORDESCRIPTION') or '')).upper()
    m = re.search(r"(\d+)\s*PTS", desc)
    if m:
        points = int(m.group(1))
        player = row.get('PLAYER1_NAME') or 'UNKNOWN'
        print(f"{player}\t{points}")
