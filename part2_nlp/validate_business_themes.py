
import csv
import sys
import random
import re
import importlib.util

csv.field_size_limit(sys.maxsize)

ARTICLES_FILE = "data/preprocessed_articles.csv"
THEMES_FILE = "data/business_themes.csv"
OUTPUT_FILE = "data/theme_validation_sample.csv"

# Import the original theme dictionary
spec = importlib.util.spec_from_file_location(
    "theme_module",
    "part2_nlp/business_theme_classification.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

THEMES = module.THEMES

random.seed(42)

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

articles = read_csv(ARTICLES_FILE)
themes = read_csv(THEMES_FILE)

article_lookup = {
    str(a["article_id"]): a
    for a in articles
}

samples = []

for theme in sorted(THEMES):
    matches = [
        row for row in themes
        if row["theme"] == theme
        and row["theme_present"] == "1"
    ]

    chosen = random.sample(
        matches, min(2, len(matches))
    )

    for row in chosen:
        article = article_lookup[str(row["article_id"])]
        text = article["article_text"]

        keyword_found = ""
        excerpt = ""

        for keyword in THEMES[theme]:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            match = re.search(pattern, text, re.I)

            if match:
                keyword_found = keyword

                start = max(0, match.start() - 180)
                end = min(len(text), match.end() + 220)

                excerpt = re.sub(
                    r"\s+", " ", text[start:end]
                )
                break

        samples.append({
            "article_id": row["article_id"],
            "title": row["title"],
            "theme": theme,
            "matched_keyword": keyword_found,
            "mention_count": row["mention_count"],
            "excerpt": excerpt,
            "manual_valid": "",
            "notes": ""
        })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=samples[0].keys()
    )
    writer.writeheader()
    writer.writerows(samples)

print("THEME VALIDATION READY")
print("=" * 45)
print("Articles in dataset:", len(articles))
print("Themes:", len(THEMES))
print("Validation samples:", len(samples))
print("Saved to:", OUTPUT_FILE)

print("\nMATCHED KEYWORDS")
for row in samples:
    print(
        row["article_id"],
        row["theme"],
        "->",
        row["matched_keyword"]
    )
