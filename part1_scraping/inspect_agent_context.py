
import csv
import sys
import re

csv.field_size_limit(sys.maxsize)

TARGET_IDS = [17, 22, 36, 43, 50, 52]

with open("data/cleaned_articles.csv", encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

pattern = re.compile(
    r"\b(?:AI agents?|agentic AI|autonomous agents?|coding agents?)\b",
    re.IGNORECASE
)

for article_id in TARGET_IDS:
    article = articles[article_id - 1]
    text = article["article_text"]

    matches = list(pattern.finditer(text))

    print("\n" + "=" * 65)
    print("ARTICLE:", article_id)
    print("TITLE:", article["title"])
    print("AGENT MENTIONS:", len(matches))

    for match in matches[:3]:
        start = max(0, match.start() - 180)
        end = min(len(text), match.end() + 250)
        excerpt = re.sub(r"\s+", " ", text[start:end])
        print("\nCONTEXT:", excerpt)

