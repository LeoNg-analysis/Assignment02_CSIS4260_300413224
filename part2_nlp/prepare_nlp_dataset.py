
import csv
import sys

csv.field_size_limit(sys.maxsize)

ARTICLES = "data/final_articles.csv"
DATES = "data/publication_date_review.csv"
MANUAL = "data/date_verification_queue.csv"
OUTPUT = "data/nlp_articles.csv"

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

articles = read_csv(ARTICLES)
dates = read_csv(DATES)
manual = read_csv(MANUAL)

# Publication dates extracted automatically
date_lookup = {
    row["url"]: row
    for row in dates
}

# Publication dates verified manually
manual_lookup = {
    row["url"]: row
    for row in manual
}

selected = []

for article in articles:
    url = article["url"]
    date_info = date_lookup.get(url, {})
    manual_info = manual_lookup.get(url, {})

    publication_date = date_info.get("publication_date", "")
    year = str(date_info.get("publication_year", "")).strip()
    status = date_info.get("date_status", "")

    manual_status = manual_info.get("verification_status", "")

    if manual_status in ("DATE_CONFIRMED", "YEAR_CONFIRMED"):
        publication_date = manual_info["verified_publication_date"]
        year = publication_date[:4]
        status = "IN_RANGE"

    if status != "IN_RANGE":
        continue

    if not year.isdigit() or not 2023 <= int(year) <= 2026:
        continue

    selected.append({
        "article_id": len(selected) + 1,
        "title": article["title"],
        "url": url,
        "publication_date": publication_date,
        "publication_year": year,
        "article_text": article["article_text"]
    })

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=selected[0].keys()
    )
    writer.writeheader()
    writer.writerows(selected)

print("Original articles:", len(articles))
print("NLP articles:", len(selected))
print("Unique URLs:", len(set(a["url"] for a in selected)))
print("Saved to:", OUTPUT)
