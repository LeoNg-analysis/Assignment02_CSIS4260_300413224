
import csv
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)

ARTICLES_FILE = "data/cleaned_articles.csv"
REVIEW_FILE = "data/relevance_review.csv"
OUTPUT_FILE = "data/final_articles.csv"

with open(ARTICLES_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

with open(REVIEW_FILE, encoding="utf-8-sig", newline="") as f:
    review_rows = list(csv.DictReader(f))

# Match by URL rather than row position
status_by_url = {
    row["url"]: row["relevance_status"]
    for row in review_rows
}

final_articles = []

for article in articles:
    status = status_by_url.get(article["url"])

    if status == "KEEP":
        final_articles.append(article)

# Save without modifying the original data
with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=articles[0].keys())
    writer.writeheader()
    writer.writerows(final_articles)

print("Original articles:", len(articles))
print("Selected articles:", len(final_articles))
print("Unique URLs:", len(set(a["url"] for a in final_articles)))
print("Excluded from final dataset:", len(articles) - len(final_articles))
print("Saved to:", OUTPUT_FILE)
