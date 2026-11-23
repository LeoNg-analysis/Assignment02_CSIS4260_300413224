
import csv

FILE = "data/date_verification_queue.csv"

verified_dates = {
    "AI Agents Are Poised to Revolutionize Employee Productivity": "2025-04-21",
    "AI Workforce: How Artificial Intelligence Is Transforming Teams": "2025-09-23"
}

with open(FILE, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

updated = 0

for row in rows:
    title = row["title"].strip()

    if title in verified_dates:
        row["verified_publication_date"] = verified_dates[title]
        row["evidence_source"] = row["url"]
        row["verification_status"] = "DATE_CONFIRMED"
        row["notes"] = "Publication date manually checked on source page"
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
