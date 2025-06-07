#!/usr/bin/env python3
import sys, csv, re

# Skip the first title line
_ = next(sys.stdin)

reader = csv.DictReader(sys.stdin)
for row in reader:
    desc = ((row.get('HOMEDESCRIPTION') or '') + (row.get('VISITORDESCRIPTION') or '')).upper()
    if re.search(r"\d+\s*PTS", desc):
        print("score\t1")
