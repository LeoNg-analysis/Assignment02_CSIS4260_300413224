
import csv

FILE = "data/date_verification_queue.csv"

verified_years = {
    "2025: The year the Frontier Firm is born": "2025",
    "2026 Work Trend Index report: Agents, human agency, and opportunity": "2026",
    "AI at Work: How human-agent teams will reshape your workforce": "2025"
}

with open(FILE, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

updated = 0

for row in rows:
    title = row["title"].strip()

    if title in verified_years:
        row["verified_publication_date"] = verified_years[title]
        row["evidence_source"] = row["url"]
        row["verification_status"] = "YEAR_CONFIRMED"
        row["notes"] = "Publication year manually checked on source page"
        updated += 1

with open(FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Updated:", updated)
print("Remaining pending:", sum(
    r["verification_status"] == "PENDING"
    for r in rows
))
