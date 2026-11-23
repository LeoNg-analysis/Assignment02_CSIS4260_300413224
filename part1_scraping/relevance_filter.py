
import csv
import sys

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/cleaned_articles.csv"
OUTPUT_FILE = "data/relevance_review.csv"

# Article numbers based on the original 63-article dataset
review_ids = {
    6, 17, 22, 36, 43, 44, 47, 50, 52, 57, 63
}

exclude_ids = {
    18, 19, 27, 39, 55
}

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

results = []

for index, article in enumerate(articles, start=1):
    if index in exclude_ids:
        status = "EXCLUDE"
    elif index in review_ids:
        status = "REVIEW"
    else:
        status = "KEEP"

    results.append({
        "article_id": index,
        "title": article["title"],
        "url": article["url"],
        "relevance_status": status
    })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

for status in ["KEEP", "REVIEW", "EXCLUDE"]:
    count = sum(r["relevance_status"] == status for r in results)
    print(f"{status}: {count}")

print("Total:", len(results))
print("Saved to:", OUTPUT_FILE)
