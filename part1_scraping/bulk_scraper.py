
import csv
import time
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
import trafilatura

BASE_DIR = Path(__file__).resolve().parent.parent
URL_FILE = BASE_DIR / "data" / "article_urls.csv"
OUTPUT_FILE = BASE_DIR / "data" / "scraped_articles.csv"

USER_AGENT = "CSIS4260StudentResearchBot"
MIN_WORDS = 200
REQUEST_DELAY = 2

FIELDNAMES = ["url", "title", "article_text"]


def read_csv(path):
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_csv(path, records, fieldnames):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def check_robots(url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    robots = RobotFileParser()
    robots.set_url(robots_url)

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=20
        )
        response.raise_for_status()
        robots.parse(response.text.splitlines())

        return robots.can_fetch(USER_AGENT, url), robots.crawl_delay(USER_AGENT)

    except requests.RequestException as error:
        print(f"Could not verify robots.txt: {error}")
        return False, None


def extract_article(url):
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=30
    )
    response.raise_for_status()

    html = response.text

    article_text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        favor_precision=True
    )

    metadata = trafilatura.extract_metadata(html)
    title = metadata.title if metadata and metadata.title else ""

    return {
        "url": url,
        "title": title,
        "article_text": article_text or ""
    }


def main():
    url_records = read_csv(URL_FILE)
    articles = read_csv(OUTPUT_FILE)

    # Keep existing articles and avoid duplicates
    existing_urls = {
        row["url"] for row in articles
        if row.get("url")
    }

    print("URLs in source list:", len(url_records))
    print("Existing articles:", len(existing_urls))

    for row in url_records:
        url = row.get("url", "").strip()

        if not url:
            continue

        if url in existing_urls:
            print(f"\nSKIPPED (already collected): {url}")
            row["status"] = "completed"
            continue

        print(f"\nProcessing: {url}")

        allowed, crawl_delay = check_robots(url)

        if not allowed:
            print("SKIPPED: robots.txt does not permit or could not be verified.")
            row["status"] = "skipped"
            continue

        try:
            article = extract_article(url)
            word_count = len(article["article_text"].split())

            if word_count < MIN_WORDS:
                print(f"SKIPPED: only {word_count} words")
                row["status"] = "skipped"
                continue

            articles.append(article)
            existing_urls.add(url)
            row["status"] = "completed"

            # Save after each successful article
            save_csv(OUTPUT_FILE, articles, FIELDNAMES)

            print(f"SAVED: {word_count} words")
            print("Title:", article["title"])

        except requests.RequestException as error:
            print("REQUEST FAILED:", error)
            row["status"] = "failed"

        except Exception as error:
            print("EXTRACTION FAILED:", error)
            row["status"] = "failed"

        finally:
            time.sleep(max(REQUEST_DELAY, crawl_delay or 0))

    save_csv(
        URL_FILE,
        url_records,
        ["url", "source", "status"]
    )

    print("\nSCRAPING COMPLETE")
    print("Total articles:", len(articles))


if __name__ == "__main__":
    main()
