
import csv
from pathlib import Path
from urllib.parse import quote

import feedparser
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "candidate_urls.csv"

SEARCH_QUERIES = {
    "Productivity & Opportunities": [
        "AI agents workplace productivity",
        "agentic AI business automation benefits"
    ],
    "Workforce Transformation": [
        "AI agents future of work workforce",
        "agentic AI employee skills job roles"
    ],
    "Job Displacement & Risks": [
        "AI agents job displacement employment risks",
        "AI agents replacing human workers"
    ],
    "Governance & Human Oversight": [
        "AI agents human oversight workplace",
        "agentic AI governance workforce risks"
    ]
}

records = []
seen_urls = set()

for topic_group, queries in SEARCH_QUERIES.items():
    for query in queries:
        rss_url = (
            "https://news.google.com/rss/search?q="
            + quote(query + " after:2023-01-01 before:2027-01-01")
            + "&hl=en-US&gl=US&ceid=US:en"
        )

        print(f"\nSearching: {query}")

        try:
            response = requests.get(
                rss_url,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0 "
                    "(compatible; CSIS4260StudentResearchBot)"
                }
            )
            response.raise_for_status()

            feed = feedparser.parse(response.content)

            print("Results found:", len(feed.entries))

            for entry in feed.entries:
                url = entry.get("link", "").strip()

                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                records.append({
                    "url": url,
                    "source": entry.get("source", {}).get(
                        "title", "Unknown"
                    ),
                    "topic_group": topic_group
                })

        except requests.RequestException as error:
            print("Search failed:", error)

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["url", "source", "topic_group"]
    )
    writer.writeheader()
    writer.writerows(records)

print("\nDISCOVERY COMPLETE")
print("Total candidate URLs:", len(records))
print("Saved to:", OUTPUT_FILE)
