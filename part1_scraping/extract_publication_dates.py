
import csv
import sys
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

csv.field_size_limit(sys.maxsize)

INPUT_FILE = "data/final_articles.csv"
OUTPUT_FILE = "data/publication_dates.csv"

HEADERS = {
    "User-Agent": "CSIS4260-AcademicResearch/1.0"
}

DATE_KEYS = [
    "article:published_time",
    "datePublished",
    "date",
    "pubdate",
    "publishdate",
    "dc.date",
    "citation_publication_date"
]

def find_jsonld_date(obj):
    if isinstance(obj, dict):
        if obj.get("datePublished"):
            return str(obj["datePublished"])
        for value in obj.values():
            found = find_jsonld_date(value)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_jsonld_date(item)
            if found:
                return found
    return None

def extract_date(soup):
    for meta in soup.find_all("meta"):
        key = (
            meta.get("property")
            or meta.get("name")
            or meta.get("itemprop")
            or ""
        ).lower()

        if key in [k.lower() for k in DATE_KEYS]:
            value = meta.get("content")
            if value:
                return value, "META"

    for script in soup.find_all(
        "script", type="application/ld+json"
    ):
        try:
            data = json.loads(script.string or script.get_text())
            date = find_jsonld_date(data)
            if date:
                return date, "JSON_LD"
        except (ValueError, TypeError):
            continue

    return "", "NOT_FOUND"

def robots_allowed(url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = RobotFileParser()
    try:
        response = requests.get(
            robots_url, headers=HEADERS, timeout=10
        )
        if response.status_code != 200:
            return False
        parser.parse(response.text.splitlines())
        return parser.can_fetch(HEADERS["User-Agent"], url)
    except requests.RequestException:
        return False

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    articles = list(csv.DictReader(f))

results = []

for i, article in enumerate(articles, 1):
    url = article["url"]
    date = ""
    method = "NOT_FOUND"

    try:
        if not robots_allowed(url):
            method = "ROBOTS_UNAVAILABLE_OR_DISALLOWED"
        else:
            response = requests.get(
                url, headers=HEADERS, timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            date, method = extract_date(soup)

    except requests.RequestException:
        method = "REQUEST_FAILED"

    results.append({
        "url": url,
        "title": article["title"],
        "publication_date": date,
        "extraction_method": method
    })

    print(f"{i}/{len(articles)} | {method} | {date}")
    time.sleep(2)

    # Save progress after every article
    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

print("\nCompleted:", len(results))
print("Saved to:", OUTPUT_FILE)
