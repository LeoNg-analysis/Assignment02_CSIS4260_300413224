
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
input_path = ROOT / "data" / "final_nlp_results.csv"
output_path = ROOT / "data" / "article_summary_scores.csv"

df = pd.read_csv(input_path)

B = df["benefit_count"].fillna(0)
C = df["challenge_count"].fillna(0)
A = df["application_count"].fillna(0)

relevance = (B + C + A) / 14
denominator = (B + C).replace(0, float("nan"))

df["importance_score"] = (
    relevance * ((B - C) / denominator).fillna(0)
).round(4)

df["importance_direction"] = df["importance_score"].apply(
    lambda score: (
        "POSITIVE" if score > 0
        else "NEGATIVE" if score < 0
        else "BALANCED"
    )
)

submission = df[
    [
        "article_id",
        "title",
        "url",
        "summary",
        "importance_score",
        "importance_direction",
        "compound_score",
        "sentiment_label",
        "benefit_count",
        "challenge_count",
        "application_count",
    ]
]

submission.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Saved: {output_path}")
print(f"Total articles: {len(submission)}")
print(submission["importance_direction"].value_counts())
print(submission[
    ["article_id", "importance_score", "importance_direction"]
].head(10).to_string(index=False))
