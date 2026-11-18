
import csv
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "candidate_urls.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    candidates = list(csv.DictReader(f))

print("Total candidates:", len(candidates))

# Test only the first 5 URLs
for i, row in enumerate(candidates[:5], start=1):
    google_url = row["url"]

    print(f"\nARTICLE {i}")
    print("Original:", google_url)
    print("Source:", row["source"])

    try:
        response = requests.get(
            google_url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15,
            allow_redirects=True
        )

        print("HTTP status:", response.status_code)
        print("Final URL:", response.url)

        if "news.google.com" in response.url:
            print("RESULT: Still a Google News URL")
        else:
            print("RESULT: Publisher URL found")

    except requests.RequestException as error:
        print("ERROR:", error)
