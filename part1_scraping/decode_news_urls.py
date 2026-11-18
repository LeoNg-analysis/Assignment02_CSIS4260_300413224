
import csv
from pathlib import Path
from urllib.parse import urlparse
from googlenewsdecoder import gnewsdecoder

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "candidate_urls.csv"
OUTPUT_FILE = BASE_DIR / "data" / "decoded_articles.csv"

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:
    candidates = list(csv.DictReader(file))

records = []
seen_urls = set()

success_count = 0
failed_count = 0

print("Total candidates:", len(candidates))

for i, row in enumerate(candidates, start=1):
    google_url = row["url"]

    print(f"\n[{i}/{len(candidates)}] {row['source']}")

    try:
        result = gnewsdecoder(
            google_url,
            interval=2
        )

        if result.get("success") is True:
            publisher_url = result.get(
                "decoded_url", ""
            ).strip()

            parsed = urlparse(publisher_url)

            if (
                parsed.scheme in ("http", "https")
                and parsed.netloc
                and parsed.netloc.lower() != "news.google.com"
            ):
                if publisher_url not in seen_urls:
                    seen_urls.add(publisher_url)

                    records.append({
                        "url": publisher_url,
                        "source": row["source"],
                        "topic_group": row["topic_group"]
                    })

                success_count += 1
                print("SUCCESS:", publisher_url)
            else:
                failed_count += 1
                print("FAILED: Invalid publisher URL")

        else:
            failed_count += 1
            print("FAILED:", result)

    except Exception as error:
        failed_count += 1
        print("ERROR:", error)

    # Save progress after each candidate
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

print("\nDECODING COMPLETE")
print("Successful decodes:", success_count)
print("Failed decodes:", failed_count)
print("Unique publisher URLs:", len(records))
print("Saved to:", OUTPUT_FILE)
