
import pandas as pd

# Input files
ARTICLES_FILE = "data/preprocessed_articles.csv"
TFIDF_FILE = "data/tfidf_keywords.csv"
SENTIMENT_FILE = "data/sentiment_results.csv"
THEMES_FILE = "data/business_themes.csv"
SUMMARIES_FILE = "data/textrank_summaries.csv"

OUTPUT_FILE = "data/final_nlp_results.csv"


def main():
    # 1. Load datasets
    articles = pd.read_csv(ARTICLES_FILE)
    tfidf = pd.read_csv(TFIDF_FILE)
    sentiment = pd.read_csv(SENTIMENT_FILE)
    themes = pd.read_csv(THEMES_FILE)
    summaries = pd.read_csv(SUMMARIES_FILE)

    # Use consistent article ID type
    datasets = [articles, tfidf, sentiment, themes, summaries]

    for df in datasets:
        df["article_id"] = df["article_id"].astype(str)

    # 2. Select article metadata
    final = articles[
        [
            "article_id",
            "title",
            "url",
            "publication_date",
            "publication_year",
            "original_word_count",
            "clean_word_count"
        ]
    ].copy()

    # 3. Aggregate top 5 TF-IDF keywords
    top_keywords = (
        tfidf.sort_values(["article_id", "keyword_rank"])
        .groupby("article_id")["keyword"]
        .apply(lambda x: ", ".join(x.head(5).astype(str)))
        .reset_index(name="top_keywords")
    )

    final = final.merge(
        top_keywords,
        on="article_id",
        how="left",
        validate="one_to_one"
    )

    # 4. Merge sentiment results
    sentiment_selected = sentiment[
        [
            "article_id",
            "compound_score",
            "sentiment_label"
        ]
    ]

    final = final.merge(
        sentiment_selected,
        on="article_id",
        how="left",
        validate="one_to_one"
    )

    # 5. Aggregate business themes
    themes["theme_present"] = (
        themes["theme_present"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    detected = themes[themes["theme_present"]].copy()

    theme_summary = (
        detected.groupby("article_id")
        .agg(
            themes_detected=(
                "theme",
                lambda x: ", ".join(sorted(x))
            ),
            theme_count=("theme", "nunique"),
            application_count=(
                "theme",
                lambda x: x.str.startswith("APPLICATION_").sum()
            ),
            benefit_count=(
                "theme",
                lambda x: x.str.startswith("BENEFIT_").sum()
            ),
            challenge_count=(
                "theme",
                lambda x: x.str.startswith("CHALLENGE_").sum()
            )
        )
        .reset_index()
    )

    final = final.merge(
        theme_summary,
        on="article_id",
        how="left",
        validate="one_to_one"
    )

    # Articles with no detected themes
    count_columns = [
        "theme_count",
        "application_count",
        "benefit_count",
        "challenge_count"
    ]

    final[count_columns] = (
        final[count_columns].fillna(0).astype(int)
    )

    final["themes_detected"] = (
        final["themes_detected"].fillna("")
    )

    # 6. Merge TextRank summaries
    summaries_selected = summaries[
        ["article_id", "summary"]
    ]

    final = final.merge(
        summaries_selected,
        on="article_id",
        how="left",
        validate="one_to_one"
    )

    # 7. Validate output
    expected_articles = len(articles)

    assert len(final) == expected_articles, (
        "Article count mismatch after merging!"
    )

    assert final["article_id"].is_unique, (
        "Duplicate article IDs detected!"
    )

    required_columns = [
        "top_keywords",
        "compound_score",
        "sentiment_label",
        "summary"
    ]

    assert final[required_columns].notna().all().all(), (
        "Missing NLP results detected!"
    )

    # 8. Save final dataset
    final.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("FINAL NLP DATASET CREATED")
    print("Total articles:", len(final))
    print("Total columns:", len(final.columns))
    print("Saved to:", OUTPUT_FILE)

    print("\nSENTIMENT DISTRIBUTION")
    print(final["sentiment_label"].value_counts())

    print("\nAVERAGE THEMES PER ARTICLE")
    print(round(final["theme_count"].mean(), 2))

    print("\nFIRST 5 ARTICLES")
    print(
        final[
            [
                "article_id",
                "title",
                "sentiment_label",
                "theme_count"
            ]
        ].head().to_string(index=False)
    )


if __name__ == "__main__":
    main()
