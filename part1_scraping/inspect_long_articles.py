
import csv
import sys
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "scraped_articles.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

for article in articles:
    text = article.get("article_text", "")
    word_count = len(text.split())

    if word_count > 10000:
        print("\n" + "=" * 60)
        print("TITLE:", article.get("title"))
        print("URL:", article.get("url"))
        print("WORD COUNT:", word_count)

        print("\nFIRST 500 CHARACTERS:")
        print(text[:500])

        print("\nMIDDLE 500 CHARACTERS:")
        middle = len(text) // 2
        print(text[middle:middle + 500])

        print("\nLAST 500 CHARACTERS:")
        print(text[-500:])
