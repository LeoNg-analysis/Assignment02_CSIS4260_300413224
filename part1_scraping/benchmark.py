
import csv
import time
from pathlib import Path
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "benchmark_urls.csv"
OUTPUT_FILE = BASE_DIR / "data" / "benchmark_results.csv"

USER_AGENT = "CSIS4260StudentResearchBot"


def allowed_by_robots(url):
    from urllib.parse import urlsplit

    parts = urlsplit(url)
    robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"

    robots = RobotFileParser()
    robots.set_url(robots_url)
    robots.read()

    return robots.can_fetch(USER_AGENT, url)


def extract_beautifulsoup(html):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1")
    title_text = title.get_text(" ", strip=True) if title else ""

    paragraphs = [
        p.get_text(" ", strip=True)
        for p in soup.find_all("p")
    ]

    text = " ".join(p for p in paragraphs if p)

    return title_text, text


def extract_scrapy(html, url):
    response = HtmlResponse(
        url=url,
        body=html.encode("utf-8"),
        encoding="utf-8",
    )

    title = response.css("h1::text").get(default="").strip()

    paragraphs = response.css("p::text").getall()
    text = " ".join(p.strip() for p in paragraphs if p.strip())

    return title, text


def main():
    with open(INPUT_FILE, encoding="utf-8-sig", newline="") as file:
        urls = [
            row["url"].strip()
            for row in csv.DictReader(file)
            if row.get("url", "").strip()
        ]

    results = []

    for url in urls:
        print(f"\nBenchmarking: {url}")

        try:
            if not allowed_by_robots(url):
                print("Skipped: robots.txt disallows scraping.")
                continue

            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=20,
            )
            response.raise_for_status()

            html = response.text

            for library, extractor in [
                ("BeautifulSoup", extract_beautifulsoup),
                ("Scrapy Selectors", extract_scrapy),
            ]:
                start = time.perf_counter()

                if library == "BeautifulSoup":
                    title, text = extractor(html)
                else:
                    title, text = extractor(html, url)

                
                elapsed = time.perf_counter() - start

                # Inspect KPMG extracted text
                if "kpmg.com" in url:
                    print(f"\n{library} - FIRST 300 CHARACTERS:")
                    print(text[:300])

                    print(f"\n{library} - LAST 300 CHARACTERS:")
                    print(text[-300:])

                results.append({
                    "url": url,
                    "library": library,
                    "parse_seconds": round(elapsed, 6),
                    "word_count": len(text.split()),
                    "success": bool(title and text),
                })

                print(
                    f"{library}: "
                    f"{elapsed:.6f}s, "
                    f"{len(text.split())} words"
                )
        except requests.RequestException as error:
            print(f"Request failed: {error}")

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "url",
                "library",
                "parse_seconds",
                "word_count",
                "success",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
