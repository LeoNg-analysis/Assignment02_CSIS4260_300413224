
import csv
import sys
import re

csv.field_size_limit(sys.maxsize)

ARTICLES_FILE = "data/cleaned_articles.csv"
REVIEW_FILE = "data/relevance_review.csv"

agent_keywords = [
    "ai agent",
    "ai agents",
    "agentic ai",
    "autonomous agent",
    "coding agent",
    "digital worker",
    "multi-agent"
]

business_keywords = [
    "business",
    "enterprise",
    "productivity",
    "automation",
    "workflow",
    "customer service",
    "operations",
    "efficiency",
    "cost",
    "revenue",
    "adoption",
    "risk"
]

with open(ARTICLES_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

with open(REVIEW_FILE, encoding="utf-8-sig", newline="") as f:
    reviews = list(csv.DictReader(f))

review_ids = {
    int(row["article_id"])
    for row in reviews
    if row["relevance_status"] == "REVIEW"
}

for article_id in sorted(review_ids):
    article = articles[article_id - 1]
    text = article["article_text"].lower()

    agent_matches = [
        keyword for keyword in agent_keywords
        if re.search(r"\b" + re.escape(keyword) + r"\b", text)
    ]

    business_matches = [
        keyword for keyword in business_keywords
        if re.search(r"\b" + re.escape(keyword) + r"\b", text)
    ]

    print("=" * 60)
    print("ARTICLE:", article_id)
    print("TITLE:", article["title"])
    print("AGENT KEYWORDS:", ", ".join(agent_matches) or "None")
    print("BUSINESS KEYWORDS:", ", ".join(business_matches) or "None")

    if agent_matches and business_matches:
        print("SUGGESTION: POTENTIAL KEEP")
    else:
        print("SUGGESTION: MANUAL REVIEW")
