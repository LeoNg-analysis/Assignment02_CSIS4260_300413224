
import csv

FILE = "data/date_verification_queue.csv"

verified_dates = {
    "How Agentic AI Is Transforming Enterprise Platforms": (
        "2025-10-13", "DATE_CONFIRMED"
    ),
    "AI Will Reshape More Jobs Than It Replaces": (
        "2026", "YEAR_CONFIRMED"
    )
}

with open(FILE, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

updated = 0

for row in rows:
    title = row["title"].strip()

    if title in verified_dates:
        date, status = verified_dates[title]

        row["verified_publication_date"] = date
        row["evidence_source"] = row["url"]
        row["verification_status"] = status
        row["notes"] = (
            "Publication date/year manually checked "
            "on the official BCG website"
        )
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
