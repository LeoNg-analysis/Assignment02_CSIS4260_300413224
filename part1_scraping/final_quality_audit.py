
import csv
import sys

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/final_articles.csv"

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

issues = []

for i, article in enumerate(articles, 1):
    title = article["title"].strip()
    text = article["article_text"].strip()
    word_count = len(text.split())

    flags = []

    if len(title) > 250:
        flags.append("LONG_TITLE")

    if word_count < 300:
        flags.append("SHORT_ARTICLE")

    if word_count > 10000:
        flags.append("VERY_LONG_ARTICLE")

    if not title or not text:
        flags.append("MISSING_CONTENT")

    if flags:
        issues.append((i, title[:80], word_count, flags))

print("Total articles:", len(articles))
print("Articles with potential issues:", len(issues))

for i, title, words, flags in issues:
    print(f"{i}. {title}")
    print(f"   Words: {words}")
    print(f"   Flags: {', '.join(flags)}")
