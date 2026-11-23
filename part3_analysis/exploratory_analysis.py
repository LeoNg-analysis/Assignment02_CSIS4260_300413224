
import pandas as pd

INPUT_FILE = "data/final_nlp_results.csv"
THEMES_FILE = "data/business_themes.csv"


def main():
    df = pd.read_csv(INPUT_FILE)
    themes = pd.read_csv(THEMES_FILE)

    print("=== DATASET OVERVIEW ===")
    print("Total articles:", len(df))
    print("Publication years:")
    print(df["publication_year"].value_counts().sort_index())

    print("\n=== SENTIMENT DISTRIBUTION ===")
    print(df["sentiment_label"].value_counts())
    print(
        "Average compound score:",
        round(df["compound_score"].mean(), 4)
    )

    print("\n=== BUSINESS THEME FREQUENCY ===")

    themes["theme_present"] = (
        themes["theme_present"]
        .astype(str)
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    theme_frequency = (
        themes[themes["theme_present"]]
        .groupby("theme")["article_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    print(theme_frequency.to_string())

    print("\n=== BUSINESS THEME CATEGORIES ===")

    for category in ["APPLICATION", "BENEFIT", "CHALLENGE"]:
        category_themes = theme_frequency[
            theme_frequency.index.str.startswith(category + "_")
        ]

        print(f"\n{category}")
        print(category_themes.to_string())

    print("\n=== AVERAGE THEME COUNTS ===")
    print(
        df[
            [
                "application_count",
                "benefit_count",
                "challenge_count"
            ]
        ].mean().round(2).to_string()
    )


if __name__ == "__main__":
    main()
