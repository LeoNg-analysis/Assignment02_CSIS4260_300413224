
import csv
import sys
import re

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/final_articles.csv"

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

year_pattern = re.compile(r"\b20(?:23|24|25|26)\b")

found = 0
missing = 0

for i, article in enumerate(articles, 1):
    # Search only the first 500 characters
    preview = article["article_text"][:500]
    years = year_pattern.findall(preview)

    if years:
        found += 1
    else:
        missing += 1
        print(f"{i:02d}. NO YEAR FOUND: {article['title'][:90]}")

print("\nTotal articles:", len(articles))
print("Articles with year mentions:", found)
print("Articles without year mentions:", missing)
