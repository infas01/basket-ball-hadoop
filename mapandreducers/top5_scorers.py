#!/usr/bin/env python3
import sys
import heapq

scores = []
for line in sys.stdin:
    player, pts = line.strip().split('\t')
    heapq.heappush(scores, (-int(pts), player))

top5 = heapq.nsmallest(5, scores)
for neg_pts, player in top5:
    print(f"{player}\t{-neg_pts}")
