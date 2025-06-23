#!/usr/bin/env python3
"""
convert_apple_watch_history.py
Convert Apple's TV-app watch-history JSON into the exact CSV layout that
Netflix exports (Title,Date with M/D/YY).  Works out-of-the-box with
ss-trakt-import.
"""

import json
import csv
import re
import sys
from datetime import datetime

IN_FILE  = sys.argv[1] if len(sys.argv) > 1 else "apple_watch.json"
OUT_FILE = sys.argv[2] if len(sys.argv) > 2 else "NetflixViewingHistory.csv"

# --- regex to pull parts out of Apple's description --------------------------------
APPLE_RX = re.compile(
    r"""
    ^(?P<show>.*?)\s*\(
      Episode\ Number:\s*\[(?P<epnum>\d+)]\s*,\s*
      Episode\ Title:\s*\[(?P<eptitle>.+?)]\s*,\s*
      Season\ Number:\s*\[(?P<season>\d+)]
    \)$
    """,
    re.VERBOSE,
)

with open(IN_FILE, encoding="utf-8") as f:
    events = json.load(f)["events"]

rows: list[dict[str, str]] = []

for ev in events:
    desc = ev["event_interpretation"]["human_readable_media_description"].strip()

    m = APPLE_RX.match(desc)
    if not m:             # skip play events that aren't TV-episode records
        continue

    show     = m.group("show")
    season   = int(m.group("season"))
    eptitle  = m.group("eptitle")

    # Netflix-style title → "Show: Season N: Episode Title"
    title = f"{show}: Season {season}: {eptitle}"

    # Convert Apple's timestamp → datetime
    ts_raw = ev["event_interpretation"]["human_readable_timestamp"]
    dt     = datetime.strptime(ts_raw, "%a %b %d %H:%M:%S GMT %Y")

    # Netflix uses M/D/YY with no leading zeros
    date   = f"{dt.month}/{dt.day}/{dt.strftime('%y')}"

    rows.append({"Title": title, "Date": date})

# keep newest first, like Netflix’s own file
rows.sort(key=lambda r: datetime.strptime(r["Date"], "%m/%d/%y"), reverse=True)

with open(OUT_FILE, "w", newline="", encoding="utf-8") as csvf:
    writer = csv.DictWriter(csvf, fieldnames=["Title", "Date"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows → {OUT_FILE}")