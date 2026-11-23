
import csv
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/preprocessed_articles.csv"
OUTPUT_FILE = "data/tfidf_keywords.csv"

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

documents = [article["clean_text"] for article in articles]

# TF-IDF configuration
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.90,
    max_features=5000,
    sublinear_tf=True
)

tfidf_matrix = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

results = []

for i, article in enumerate(articles):
    scores = tfidf_matrix[i].toarray().ravel()
    top_indices = np.argsort(scores)[::-1][:15]

    for rank, idx in enumerate(top_indices, 1):
        results.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "keyword_rank": rank,
            "keyword": feature_names[idx],
            "tfidf_score": round(float(scores[idx]), 6)
        })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("TF-IDF ANALYSIS COMPLETED")
print("=" * 40)
print("Articles analyzed:", len(articles))
print("TF-IDF matrix shape:", tfidf_matrix.shape)
print("Keywords extracted:", len(results))
print("Saved to:", OUTPUT_FILE)

print("\nTOP 15 KEYWORDS - FIRST ARTICLE")
for row in results[:15]:
    print(
        f"{row['keyword_rank']:2}. "
        f"{row['keyword']:<30} "
        f"{row['tfidf_score']:.4f}"
    )

