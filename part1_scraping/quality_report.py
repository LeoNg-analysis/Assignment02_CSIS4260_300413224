
import csv
import sys
from pathlib import Path
from urllib.parse import urlparse

csv.field_size_limit(sys.maxsize)

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "scraped_articles.csv"
OUTPUT_FILE = BASE_DIR / "data" / "quality_report.csv"

KEYWORDS = [
    "ai agent",
    "agentic ai",
    "workforce",
    "employee",
    "productivity",
    "automation",
    "job",
    "human oversight"
]

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

report = []

for article in articles:
    url = article.get("url", "")
    title = article.get("title", "")
    text = article.get("article_text", "")

    word_count = len(text.split())
    text_lower = text.lower()

    matched_keywords = [
        keyword
        for keyword in KEYWORDS
        if keyword in text_lower
    ]

    if word_count > 10000:
        status = "REVIEW"
    elif word_count < 500 or len(matched_keywords) < 2:
        status = "REVIEW"
    else:
        status = "PASS"

    report.append({
        "source": urlparse(url).netloc,
        "title": title,
        "word_count": word_count,
        "keyword_count": len(matched_keywords),
        "quality_status": status,
        "url": url
    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "source",
            "title",
            "word_count",
            "keyword_count",
            "quality_status",
            "url"
        ]
    )
    writer.writeheader()
    writer.writerows(report)

print("\nQUALITY REPORT")
print("Total articles:", len(report))

for row in report:
    print(
        row["quality_status"],
        "|",
        row["word_count"],
        "words |",
        row["keyword_count"],
        "keywords |",
        row["source"]
    )

print("\nPASS:", sum(r["quality_status"] == "PASS" for r in report))
print("REVIEW:", sum(r["quality_status"] == "REVIEW" for r in report))
print("Saved to:", OUTPUT_FILE)
