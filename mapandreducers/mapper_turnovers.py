#!/usr/bin/env python3
import sys, csv

# Skip the first title line
_ = next(sys.stdin)

reader = csv.DictReader(sys.stdin)
for row in reader:
    desc = ((row.get('HOMEDESCRIPTION') or '') + (row.get('VISITORDESCRIPTION') or '')).upper()
    if 'TURNOVER' in desc:
        team = row.get('PLAYER1_TEAM_ABBREVIATION') or 'UNKNOWN'
        print(f"{team}\t1")
