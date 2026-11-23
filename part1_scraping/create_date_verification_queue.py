
import csv

INPUT_FILE = "data/publication_date_review.csv"
OUTPUT_FILE = "data/date_verification_queue.csv"

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

queue = []

for article in articles:
    if article["date_status"] != "NEEDS_REVIEW":
        continue

    queue.append({
        "title": article["title"],
        "url": article["url"],
        "extraction_method": article["extraction_method"],
        "verified_publication_date": "",
        "evidence_source": "",
        "verification_status": "PENDING",
        "notes": ""
    })

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=queue[0].keys())
    writer.writeheader()
    writer.writerows(queue)

print("Articles requiring verification:", len(queue))
print("Saved to:", OUTPUT_FILE)
