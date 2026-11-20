
import csv
from pathlib import Path
import sys

limit = sys.maxsize

while True:
    try:
        csv.field_size_limit(limit)
        break
    except OverflowError:
        limit //= 10
BASE_DIR = Path(__file__).resolve().parent.parent

DECODED_FILE = BASE_DIR / "data" / "decoded_articles.csv"
QUEUE_FILE = BASE_DIR / "data" / "article_urls.csv"
DATASET_FILE = BASE_DIR / "data" / "scraped_articles.csv"

TEST_LIMIT = 20


def read_csv(path):
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


decoded = read_csv(DECODED_FILE)
queue = read_csv(QUEUE_FILE)
articles = read_csv(DATASET_FILE)

existing_urls = {
    row["url"] for row in queue if row.get("url")
}

collected_urls = {
    row["url"] for row in articles if row.get("url")
}

added = 0

for row in decoded:
    url = row.get("url", "").strip()

    if not url or url in existing_urls:
        continue

    queue.append({
        "url": url,
        "source": row.get("source", "Unknown"),
        "status": (
            "completed"
            if url in collected_urls
            else "pending"
        )
    })

    existing_urls.add(url)
    added += 1

    if added >= TEST_LIMIT:
        break

with open(
    QUEUE_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["url", "source", "status"]
    )
    writer.writeheader()
    writer.writerows(queue)

print("Decoded URLs:", len(decoded))
print("New URLs added:", added)
print("Total queue:", len(queue))
print("Already collected:", len(collected_urls))
print("Saved to:", QUEUE_FILE)
