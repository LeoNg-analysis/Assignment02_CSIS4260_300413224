
import csv
import sys
import re
from collections import Counter

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/preprocessed_articles.csv"
OUTPUT_FILE = "data/business_themes.csv"

THEMES = {
    "APPLICATION_Customer_Service": [
        "customer service", "customer support",
        "customer experience", "chatbot", "support ticket"
    ],
    "APPLICATION_Sales": [
        "sales", "lead generation", "sales pipeline",
        "customer acquisition"
    ],
    "APPLICATION_Marketing": [
        "marketing", "advertising", "campaign",
        "content creation"
    ],
    "APPLICATION_Operations": [
        "operations", "business process",
        "workflow", "supply chain", "logistics"
    ],
    "APPLICATION_Data_Analytics": [
        "data analytics", "data analysis",
        "business intelligence", "predictive analytics"
    ],
    "BENEFIT_Productivity": [
        "productivity", "time saving", "time savings",
        "faster", "efficiency"
    ],
    "BENEFIT_Cost_Efficiency": [
        "cost reduction", "reduce costs",
        "cost savings", "lower costs"
    ],
    "BENEFIT_Automation": [
        "automation", "automate", "automated",
        "autonomous"
    ],
    "BENEFIT_Decision_Making": [
        "decision making", "decision support",
        "informed decisions", "decision intelligence"
    ],
    "CHALLENGE_Security": [
        "security", "privacy", "data protection",
        "cybersecurity", "access control"
    ],
    
"CHALLENGE_Cost": [
    "implementation cost",
    "implementation costs",
    "deployment cost",
    "deployment costs",
    "high costs",
    "cost barrier",
    "financial burden",
    "expensive deployment",
    "expensive deployments",
    "budget constraints",
    "ballooning costs",
    "unpredictable costs",
    "resource consumption",
    "cost management",
    "costly integration",
    "expensive overhaul"
],

"CHALLENGE_Reliability": [
    "hallucination",
    "hallucinations",
    "inaccurate results",
    "incorrect outputs",
    "ai errors",
    "agent errors",
    "unreliable",
    "irregular reliability",
    "lack of accuracy",
    "faulty information",
    "catch mistakes",
    "fewer errors",
    "mistakes can spread",
    "errors must be understood",
    "don't trust the accuracy"
],

"CHALLENGE_Integration": [
    "integration challenges",
    "integration difficulties",
    "integration issues",
    "integration barriers",
    "legacy system integration",
    "legacy systems",
    "weak data integration",
    "poor integration",
    "complex integration",
    "costly integration",
    "system compatibility",
    "integration with such legacy technology",
    "integration of legacy systems"
],

    "CHALLENGE_Human_Oversight": [
        "human oversight", "human intervention",
        "human supervision", "human in the loop"
    ]
}

def count_theme_mentions(text, keywords):
    total = 0

    for keyword in keywords:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        total += len(re.findall(pattern, text))

    return total

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

results = []
theme_frequency = Counter()

for article in articles:
    text = article["article_text"].lower()

    for theme, keywords in THEMES.items():
        mentions = count_theme_mentions(text, keywords)
        present = int(mentions > 0)

        theme_frequency[theme] += present

        results.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "theme": theme,
            "mention_count": mentions,
            "theme_present": present
        })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=results[0].keys()
    )
    writer.writeheader()
    writer.writerows(results)

print("BUSINESS THEME CLASSIFICATION COMPLETED")
print("=" * 45)
print("Articles analyzed:", len(articles))
print("Themes:", len(THEMES))
print("Records generated:", len(results))
print("Saved to:", OUTPUT_FILE)

print("\nTHEME FREQUENCY")
for theme, count in theme_frequency.most_common():
    print(f"{theme}: {count}/{len(articles)}")
