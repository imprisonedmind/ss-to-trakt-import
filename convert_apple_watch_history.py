import json
import csv
from datetime import datetime

with open('apple_watch.json') as f:
    data = json.load(f)['events']

rows = []
for ev in data:
    interp = ev['event_interpretation']
    title = interp['human_readable_media_description']
    ts = interp['human_readable_timestamp']  # e.g. "Sun May 25 18:52:10 GMT 2025"
    dt = datetime.strptime(ts, '%a %b %d %H:%M:%S GMT %Y')
    rows.append({
        'Title': title,
        'Date': dt.strftime('%m/%d/%Y')
    })

# write CSV
with open('watch_history_netflix.csv', 'w', newline='') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=['Title','Date'])
    writer.writeheader()
    writer.writerows(rows)