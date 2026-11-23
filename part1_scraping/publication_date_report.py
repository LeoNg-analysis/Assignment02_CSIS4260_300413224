
import csv
from collections import Counter
from datetime import datetime

INPUT_FILE = "data/publication_dates.csv"
OUTPUT_FILE = "data/publication_date_review.csv"

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

results = []
year_counts = Counter()
status_counts = Counter()

for article in articles:
    raw_date = article["publication_date"].strip()
    method = article["extraction_method"]

    year = ""
    status = "NEEDS_REVIEW"

    if raw_date:
        try:
            # Support ISO, YYYYMMDD, and written dates
            if len(raw_date) >= 4 and raw_date[:4].isdigit():
                year = int(raw_date[:4])
            else:
                for fmt in ["%B %d, %Y", "%b %d, %Y"]:
                    try:
                        year = datetime.strptime(
                            raw_date, fmt
                        ).year
                        break
                    except ValueError:
                        continue

            if isinstance(year, int):
                if 2023 <= year <= 2026:
                    status = "IN_RANGE"
                else:
                    status = "OUT_OF_RANGE"

                year_counts[year] += 1

        except (ValueError, TypeError):
            pass

    status_counts[status] += 1

    results.append({
        **article,
        "publication_year": year,
        "date_status": status
    })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=results[0].keys()
    )
    writer.writeheader()
    writer.writerows(results)

print("PUBLICATION DATE REPORT")
print("=" * 45)

for year in sorted(year_counts):
    print(f"{year}: {year_counts[year]} articles")

print("\nSTATUS")
for status, count in status_counts.items():
    print(f"{status}: {count}")

print("\nARTICLES REQUIRING REVIEW")
for i, article in enumerate(results, 1):
    if article["date_status"] != "IN_RANGE":
        print(
            f"{i}. {article['title'][:75]} "
            f"| {article['extraction_method']}"
        )

print("\nSaved to:", OUTPUT_FILE)
