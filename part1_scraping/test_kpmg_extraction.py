
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

URL = (
    "https://kpmg.com/us/en/articles/2025/"
    "ai-agents-shaping-talent-strategy.html"
)

USER_AGENT = "CSIS4260StudentResearchBot"

#Check robots.txt
robots = RobotFileParser()
robots.set_url("https://kpmg.com/robots.txt")
robots.read()

if not robots.can_fetch(USER_AGENT, URL):
    raise SystemExit("Scraping not allowed.")

#Download HTML
response = requests.get(
    URL,
    headers={"User-Agent": USER_AGENT},
    timeout=20
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

#Identify the main page content
main = soup.find("main")

if main is None:
    raise SystemExit("Main content not found.")

start_heading = "How AI Demands Innovative Approaches to Talent Decisions"
end_heading = "Working with KPMG"

start_found = False
end_found = False
paragraphs = []

#Read elements in HTML document order
for element in main.find_all(
    ["h2", "h3", "h4", "p", "li"]
):
    text = element.get_text(" ", strip=True)

    if element.name == "h2" and text == start_heading:
        start_found = True

    if element.name == "h2" and text == end_heading:
        end_found = True
        break

    if start_found and text:
        # Avoid duplicating text nested inside list items
        if element.name == "p" and element.find_parent("li"):
            continue

        paragraphs.append(text)

if not start_found or not end_found:
    raise SystemExit(
        "Expected article boundaries not found. "
        "Review the page structure."
    )

print("\nLIST ELEMENTS IN MAIN:")

for list_tag in main.find_all(["ul", "ol"]):
    items = [
        li.get_text(" ", strip=True)
        for li in list_tag.find_all("li", recursive=False)
    ]

    if items:
        print("\nLIST:")
        for item in items[:5]:
            print("-", item[:180])


article_text = " ".join(paragraphs)

#Remove the promotional closing paragraph
promotional_ending = (
    "Now is the time to act and position your "
    "organization for long-term success."
)

if promotional_ending in article_text:
    article_text = article_text.split(
        promotional_ending, 1
    )[0].strip()
else:
    print("WARNING: Promotional ending not found.")


print("\nKPMG ARTICLE EXTRACTION")
print("Word count:", len(article_text.split()))

print("\nFIRST 500 CHARACTERS:")
print(article_text[:500])

print("\nLAST 500 CHARACTERS:")
print(article_text[-500:])


# Step 7: Save KPMG article to dataset
import csv
from pathlib import Path

output_file = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "scraped_articles.csv"
)

# Get article title
title = soup.find("h1")
title_text = title.get_text(" ", strip=True) if title else ""

# Load existing dataset
records = []

if output_file.exists():
    with open(
        output_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        reader = csv.DictReader(f)
        records = list(reader)

# Remove old KPMG record if it exists
records = [
    row for row in records
    if row.get("url") != URL
]

# Add cleaned KPMG article
records.append({
    "url": URL,
    "title": title_text,
    "article_text": article_text
})

# Save dataset
with open(
    output_file,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["url", "title", "article_text"]
    )
    writer.writeheader()
    writer.writerows(records)

print("\nDataset updated!")
print("Total articles:", len(records))
print("KPMG words:", len(article_text.split()))
print("Saved to:", output_file)
