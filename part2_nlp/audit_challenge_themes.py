
import csv
import sys
import re
sys.stdout.reconfigure(encoding="utf-8")

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/preprocessed_articles.csv"

KEYWORDS = {
    "CHALLENGE_Cost": [
        "cost", "expensive", "budget", "investment",
        "financial", "pricing"
    ],
    "CHALLENGE_Reliability": [
        "accuracy", "errors", "mistakes",
        "reliability", "hallucination"
    ],
    "CHALLENGE_Integration": [
        "integration", "integrate", "legacy",
        "implementation", "interoperability"
    ]
}

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

for theme, keywords in KEYWORDS.items():
    print("\n" + "=" * 60)
    print(theme)
    print("=" * 60)

    count = 0

    for article in articles:
        text = article["article_text"]

        matches = []

        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            for match in re.finditer(pattern, text, re.I):
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 150)

                excerpt = re.sub(
                    r"\s+", " ", text[start:end]
                )

                matches.append((keyword, excerpt))

        if matches:
            count += 1

            print(
                f"\nArticle {article['article_id']}: "
                f"{article['title'][:65]}"
            )

            for keyword, excerpt in matches[:2]:
                print("Keyword:", keyword)
                print("Context:", excerpt[:250])

    print(f"\nArticles with broad keyword matches: {count}")
