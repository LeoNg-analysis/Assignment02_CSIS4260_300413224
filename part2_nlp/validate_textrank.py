
import csv
import random
import sys

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/textrank_summaries.csv"
OUTPUT_FILE = "data/textrank_validation_sample.csv"

random.seed(42)

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

sample = random.sample(
    articles,
    min(10, len(articles))
)

results = []

for article in sample:
    results.append({
        "article_id": article["article_id"],
        "title": article["title"],
        "summary": article["summary"],
        "relevance_score": "",
        "readability_score": "",
        "notes": ""
    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)

print("TEXTRANK VALIDATION SAMPLE CREATED")
print("Total articles:", len(articles))
print("Sample size:", len(results))
print("Saved to:", OUTPUT_FILE)
