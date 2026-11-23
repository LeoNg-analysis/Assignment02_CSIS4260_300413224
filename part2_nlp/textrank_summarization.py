
import csv
import re
import sys

import networkx as nx
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/preprocessed_articles.csv"
OUTPUT_FILE = "data/textrank_summaries.csv"


def split_sentences(text):
    # Normalize whitespace
    text = text.replace("\xa0", " ")

    # Fix some known encoding artifacts
    text = text.replace("â18", "–18")

    # Split text into sentences
    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    cleaned = []

    for sentence in sentences:
        sentence = re.sub(r"\s+", " ", sentence).strip()
        word_count = len(sentence.split())

        # Exclude short headings and excessively long sentences
        if not 12 <= word_count <= 65:
            continue

        # Exclude numbered fragments
        if re.match(r"^\d+\s*[|.)]", sentence):
            continue

        # Exclude bullet fragments
        if sentence.startswith(("-", "•")):
            continue

        cleaned.append(sentence)

    return cleaned


def textrank_summary(text, top_n=3):
    sentences = split_sentences(text)

    if len(sentences) <= top_n:
        return " ".join(sentences), len(sentences)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(sentences)
    except ValueError:
        return " ".join(sentences[:top_n]), len(sentences)

    similarity_matrix = cosine_similarity(tfidf_matrix)
    np.fill_diagonal(similarity_matrix, 0)

    graph = nx.from_numpy_array(similarity_matrix)

    try:
        scores = nx.pagerank(
            graph,
            weight="weight",
            max_iter=200
        )
    except nx.PowerIterationFailedConvergence:
        return " ".join(sentences[:top_n]), len(sentences)

    
    # Maximal Marginal Relevance (MMR)
    # Balance sentence importance and diversity
    lambda_param = 0.65

    selected_indices = []
    remaining_indices = set(range(len(sentences)))

    while remaining_indices and len(selected_indices) < top_n:
        best_idx = None
        best_score = float("-inf")

        for idx in sorted(remaining_indices):
            relevance = scores[idx]

            if selected_indices:
                redundancy = max(
                    similarity_matrix[idx, selected_idx]
                    for selected_idx in selected_indices
                )
            else:
                redundancy = 0.0

            mmr_score = (
                lambda_param * relevance
                - (1 - lambda_param) * redundancy
            )

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx

        selected_indices.append(best_idx)
        remaining_indices.remove(best_idx)

    # Restore original sentence order
    ranked_indices = sorted(selected_indices)


    summary = " ".join(
        sentences[i] for i in ranked_indices
    )

    return summary, len(sentences)


def main():
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        articles = list(csv.DictReader(file))

    results = []

    for article in articles:
        summary, sentence_count = textrank_summary(
            article["article_text"]
        )

        results.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "url": article["url"],
            "summary": summary,
            "sentence_count": sentence_count,
            "summary_sentence_count": min(3, sentence_count)
        })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "article_id",
                "title",
                "url",
                "summary",
                "sentence_count",
                "summary_sentence_count"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("TEXTRANK SUMMARIZATION COMPLETED")
    print("Articles summarized:", len(results))
    print("Saved to:", OUTPUT_FILE)

    print("\nFIRST ARTICLE SUMMARY")
    print("Title:", results[0]["title"])
    print("Summary:", results[0]["summary"])


if __name__ == "__main__":
    main()
