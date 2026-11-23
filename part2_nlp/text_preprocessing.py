
import csv
import sys
import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/nlp_articles.csv"
OUTPUT_FILE = "data/preprocessed_articles.csv"

# Preserve important research terms
important_terms = {
    "ai", "agent", "agents", "agentic",
    "automation", "business", "productivity",
    "workforce", "cost", "risk", "human"
}

stopwords = set(ENGLISH_STOP_WORDS) - important_terms

def preprocess_text(text):
    text = text.lower()

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Keep alphabetic words
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra whitespace
    tokens = text.split()

    # Remove stopwords and single-character tokens
    tokens = [
        token for token in tokens
        if token not in stopwords and len(token) > 1
    ]

    return " ".join(tokens)

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

processed = []

for article in articles:
    original_text = article["article_text"]
    clean_text = preprocess_text(original_text)

    processed.append({
        **article,
        "clean_text": clean_text,
        "original_word_count": len(original_text.split()),
        "clean_word_count": len(clean_text.split())
    })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=processed[0].keys()
    )
    writer.writeheader()
    writer.writerows(processed)

print("TEXT PREPROCESSING COMPLETED")
print("=" * 40)
print("Articles processed:", len(processed))
print("Output:", OUTPUT_FILE)

avg_original = sum(
    a["original_word_count"] for a in processed
) / len(processed)

avg_clean = sum(
    a["clean_word_count"] for a in processed
) / len(processed)

print("Average original words:", round(avg_original, 2))
print("Average cleaned words:", round(avg_clean, 2))
print(
    "Word reduction:",
    round((1 - avg_clean / avg_original) * 100, 2),
    "%"
)

print("\nSAMPLE")
print("Title:", processed[0]["title"])
print("Clean text preview:", processed[0]["clean_text"][:400])

