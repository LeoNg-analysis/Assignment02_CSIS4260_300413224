
import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "data/final_nlp_results.csv"
THEMES_FILE = "data/business_themes.csv"
OUTPUT_DIR = "part3_analysis/figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_FILE)
themes = pd.read_csv(THEMES_FILE)

themes["theme_present"] = (
    themes["theme_present"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(["true", "1", "yes"])
)

frequency = (
    themes[themes["theme_present"]]
    .groupby("theme")["article_id"]
    .nunique()
    .sort_values()
)

# Figure 1: Business themes
fig, ax = plt.subplots(figsize=(11, 7))

frequency.plot.barh(ax=ax)

ax.set_title("AI Agents: Business Theme Frequency")
ax.set_xlabel("Number of Articles")
ax.set_ylabel("Business Theme")
ax.set_xlim(0, len(df))

plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/business_theme_frequency.png",
    dpi=300
)
plt.close()

# Figure 2: Sentiment distribution
sentiment_counts = (
    df["sentiment_label"]
    .value_counts()
)

fig, ax = plt.subplots(figsize=(7, 5))

sentiment_counts.plot.bar(ax=ax)

ax.set_title("VADER Sentiment Distribution")
ax.set_xlabel("Sentiment")
ax.set_ylabel("Number of Articles")
ax.set_ylim(0, len(df) + 5)

plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/sentiment_distribution.png",
    dpi=300
)
plt.close()

# Figure 3: Publication year
year_counts = (
    df["publication_year"]
    .value_counts()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(7, 5))

year_counts.plot.bar(ax=ax)

ax.set_title("Articles by Publication Year")
ax.set_xlabel("Publication Year")
ax.set_ylabel("Number of Articles")

plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/publication_year.png",
    dpi=300
)
plt.close()

print("VISUALIZATIONS CREATED")
print("Saved to:", OUTPUT_DIR)
print("Total figures: 3")
