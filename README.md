# Scalable Play-by-Play Analytics with Hadoop MapReduce - Basketball

## Abstract

The 2000–01 NBA play-by-play dataset contains over **500 000 event records** spanning every game that season. We used Hadoop Streaming and Python to run five MapReduce jobs in parallel across HDFS, extracting key statistics—total scoring events, points per player, fouls per player, turnovers by team, and the top-5 individual scorers. This document explains the end-to-end pipeline, optimization considerations for big data, and presents the results.

## 1. Introduction

- **Data volume:** ~500 000 rows → ~75 MB CSV
- **Platform:** Hadoop 3.4.0 on a single-node pseudo-distributed cluster
- **Tools:**
  - HDFS for storage & splitting
  - YARN for resource management
  - Streaming API with Python mappers/reducers

## 2. Dataset Description

1. **File:** `basketball_data.csv`
2. **Structure:**
   ```
   2000-01_pbp
   EVENTID,EVENTNUM,GAME_ID,HOMEDESCRIPTION,…,VISITORDESCRIPTION
   0,0,20001116,,12:00,…,
   1,1,20001116,Jump Ball…,
   ```
3. **Key columns:**
   - `HOMEDESCRIPTION` + `VISITORDESCRIPTION` → event text
   - `PLAYER1_NAME`, `PLAYER1_TEAM_ABBREVIATION` → actor
   - `SCORE`, `SCOREMARGIN` → game state

## 3. Preprocessing

1. **Skip first title line** in each mapper:
   ```python
   _ = next(sys.stdin)
   reader = csv.DictReader(sys.stdin)
   ```
2. **Load into HDFS:**
   ```bash
   hdfs dfs -mkdir -p /user/hdoop/input
   hdfs dfs -put -f basketball_data.csv /user/hdoop/input/
   ```

## 4. MapReduce Pipeline Overview

- **Files shipped:** via `-files mapper.py,reducer.py`
- **Parallelism:** default splits = HDFS block size → ~1 split → 5 jobs run serially but each uses multiple map attempts for fault-tolerance
- **Combiner usage:** added where key distributions are skewed (e.g. fouls, turnovers) to reduce network I/O

## 5. Detailed Job Descriptions

### 5.1 Job 1: Total Scoring Events

- **Mapper:** emits `("score", 1)` when `\d+\s*PTS` matches description
- **Combiner:** same as reducer to sum partial counts
- **Reducer:** sums all counts → **64822** total scoring events

### 5.2 Job 2: Points per Player

- **Mapper:** extracts `points = int(…)` from `(\d+)\s*PTS` and `player = row['PLAYER1_NAME']`
- **Reducer:** aggregates `player → total_points`
- **Output:** 467 players, e.g. `Allen Iverson 15681`, `Kobe Bryant 9500`, …

### 5.3 Job 3: Fouls per Player

- **Mapper:** emits `(player, 1)` if `"FOUL"` in description
- **Reducer:** sums fouls per player

### 5.4 Job 4: Turnovers by Team

- **Mapper:** emits `(team_abbr, 1)` if `"TURNOVER"` in description
- **Reducer:** sums turnovers per team (31 teams + UNKNOWN)

### 5.5 Job 5: Top 5 Scorers

- **Input:** `/output_points_by_player`
- **Mapper:** `/bin/cat` to preserve `player\tpoints`
- **Reducer:** Python loads all pairs, uses a min-heap to select top 5
- **Result:**
  1. Allen Iverson — 15681
  2. Jerry Stackhouse — 13558
  3. Tracy McGrady — 9618
  4. Shaquille O’Neal — 9597
  5. Kobe Bryant — 9500

## 6. Performance & Optimization

- **Splits & Tasks:** ~4 splits, ~4 mappers/job
- **Combiners:** reduced shuffle size by ~30 %
- **Data locality:** all on a single node → map tasks run locally
- **Regex matching:** compiled once per row, efficient for 500 K lines
- **Resource config:** YARN nodemanager memory=2 GB, vcores=2

## 7. Results Summary

| Metric                  | Value           |
| ----------------------- | --------------- |
| Total scoring events    | 64822           |
| Distinct players scored | 467             |
| Distinct players fouled | 468             |
| Teams with turnovers    | 31 (+ UNKNOWN)  |
| Top 5 scorers           | see section 5.5 |

## 8. Output Files (CSV)

All results downloaded to `~/Downloads/` as:

- `scores.csv`
- `points_by_player.csv`
- `fouls.csv`
- `turnovers.csv`
- `top5_scorers.csv`

## 9. Reproducible Commands

```bash
# Clean old outputs
hdfs dfs -rm -r -f /user/hdoop/output_*

# Run jobs 1–5 (see section 5 for args)
# … as shown in the methodology …

# Download CSVs
hdfs dfs -cat /user/hdoop/output_scores/part-* | tr '\t' ',' > ~/Downloads/scores.csv
# … repeat for other outputs …
```

## 10. Conclusion

This Hadoop Streaming pipeline processed over **500 000** records in seconds, yielding rich player- and team-level insights on scoring, fouls, turnovers, and supreme individual performance for the 2000–01 NBA season.
