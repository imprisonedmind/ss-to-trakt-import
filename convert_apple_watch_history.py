#!/usr/bin/env python3
"""
apple2netflix_csv.py
Convert Apple's watch-activity JSON into a Netflix-style ViewingActivity.csv
ready for ss-trakt-import.

Usage:
    python apple2netflix_csv.py [input.json] [output.csv]

If no args are given it defaults to apple_watch.json → NetflixViewingHistory.csv
"""

import json
import csv
import sys
from datetime import datetime

IN_FILE  = sys.argv[1] if len(sys.argv) > 1 else "apple_watch.json"
OUT_FILE = sys.argv[2] if len(sys.argv) > 2 else "NetflixViewingHistory.csv"

with open(IN_FILE, encoding="utf-8") as f:
    events = json.load(f)["events"]

rows = []
for ev in events:
    interp = ev["event_interpretation"]
    title = interp["human_readable_media_description"].strip()

    # Example timestamp: "Sun May 25 18:52:10 GMT 2025"
    ts_raw = interp["human_readable_timestamp"]
    dt = datetime.strptime(ts_raw, "%a %b %d %H:%M:%S GMT %Y")

    # ss-trakt-import first tries "%d.%m.%y", so produce that
    date_for_trakt = dt.strftime("%d.%m.%y")

    rows.append({"Title": title, "Date": date_for_trakt})

# Optional: sort chronologically (oldest → newest)
rows.sort(key=lambda r: datetime.strptime(r["Date"], "%d.%m.%y"))

with open(OUT_FILE, "w", newline="", encoding="utf-8") as csvf:
    writer = csv.DictWriter(csvf, fieldnames=["Title", "Date"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUT_FILE}")