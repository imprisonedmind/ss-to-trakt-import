# prime_to_netflix_csv.py  –  outputs exactly:
# "Title","M/D/YY"

from bs4 import BeautifulSoup
from datetime import datetime
import csv, pathlib

in_file  = pathlib.Path("prime_watch_history.html")
out_file = pathlib.Path("NetflixViewingHistory.csv")

soup = BeautifulSoup(in_file.read_text(encoding="utf-8"), "html.parser")
rows = []

# 1️⃣ walk every date section
for date_hdr in soup.select('div[data-automation-id^="wh-date-"]'):
    nice_date  = date_hdr.get_text(strip=True)                 # June 15, 2025
    slash_date = datetime.strptime(nice_date, "%B %d, %Y").strftime("%-m/%-d/%y")

    # 2️⃣ every watch item under that date
    for item in date_hdr.find_parent("li").select("ul > li.avarm3"):
        title_a = item.select_one("div.ITFX06 a, div._6YbHut a")
        show    = title_a.get_text(" ", strip=True) if title_a else ""

        # episodes called out individually
        eps = item.select("ul li._4yED5J")
        if eps:
            for ep in eps:
                rows.append([f"{show}: {ep.p.get_text(' ', strip=True)}", slash_date])
        else:
            rows.append([show, slash_date])

# 3️⃣ write Netflix-style CSV – no header, every field quoted
with out_file.open("w", newline="", encoding="utf-8") as f:
    csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)

print(f"✓ Wrote {len(rows)} rows to {out_file}")
