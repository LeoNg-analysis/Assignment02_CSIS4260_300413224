
import csv
import sys
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/preprocessed_articles.csv"
OUTPUT_FILE = "data/sentiment_results.csv"

nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()

def split_sentences(text):
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if len(sentence.split()) >= 5
    ]

def analyze_article(text):
    sentences = split_sentences(text)

    if not sentences:
        return None

    scores = [
        sia.polarity_scores(sentence)
        for sentence in sentences
    ]

    avg_compound = sum(
        score["compound"] for score in scores
    ) / len(scores)

    avg_positive = sum(
        score["pos"] for score in scores
    ) / len(scores)

    avg_negative = sum(
        score["neg"] for score in scores
    ) / len(scores)

    avg_neutral = sum(
        score["neu"] for score in scores
    ) / len(scores)

    if avg_compound >= 0.05:
        label = "POSITIVE"
    elif avg_compound <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return {
        "sentence_count": len(sentences),
        "positive_score": round(avg_positive, 4),
        "negative_score": round(avg_negative, 4),
        "neutral_score": round(avg_neutral, 4),
        "compound_score": round(avg_compound, 4),
        "sentiment_label": label
    }

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

results = []

for article in articles:
    sentiment = analyze_article(article["article_text"])

    if sentiment is None:
        print("Skipped:", article["title"])
        continue

    results.append({
        "article_id": article["article_id"],
        "title": article["title"],
        "url": article["url"],
        **sentiment
    })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=results[0].keys()
    )
    writer.writeheader()
    writer.writerows(results)

print("VADER SENTIMENT ANALYSIS COMPLETED")
print("=" * 45)
print("Articles analyzed:", len(results))
print("Saved to:", OUTPUT_FILE)

print("\nSENTIMENT DISTRIBUTION")

for label in ["POSITIVE", "NEUTRAL", "NEGATIVE"]:
    count = sum(
        r["sentiment_label"] == label
        for r in results
    )
    print(f"{label}: {count}")

print("\nFIRST 5 ARTICLES")

for article in results[:5]:
    print(
        article["article_id"],
        article["sentiment_label"],
        article["compound_score"],
        article["title"][:55]
    )

