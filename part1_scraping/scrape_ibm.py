
import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.robotparser import RobotFileParser

URL = "https://www.ibm.com/think/topics/ai-agents"
USER_AGENT = "CSIS4260StudentResearchBot"

#Check robots.txt
robots = RobotFileParser()
robots.set_url("https://www.ibm.com/robots.txt")
robots.read()

if not robots.can_fetch(USER_AGENT, URL):
    raise SystemExit("Scraping is not allowed for this URL.")

#Download HTML
response = requests.get(
    URL,
    headers={"User-Agent": USER_AGENT},
    timeout=20
)
response.raise_for_status()

#Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

title = soup.find("h1")
title_text = (
    title.get_text(" ", strip=True)
    if title else ""
)

for tag in soup.select(
    ".cta-section-wrapper, "
    "c4d-cta-block, "
    "c4d-cta-block-item"
):
    tag.decompose()

#Find heading
resources_heading = soup.find(
    lambda tag: (
        tag.name in ["h2", "h3", "h4", "h5", "h6"]
        and tag.get_text(" ", strip=True).lower()
        == "resources"
    )
)


#Extract article text
paragraphs = []

for element in soup.find_all(
    ["p", "h2", "h3", "h4", "h5", "h6"]
):

    text = element.get_text(" ", strip=True)

    #Stop at Resources section
    if (
        resources_heading is not None
        and element is resources_heading
    ):
        break

    #Stop at author section, if identified
    if (
        element.name in ["h2", "h3", "h4", "h5", "h6"]
        and text.lower() == "author"
    ):
        break

    if text:
        paragraphs.append(text)


article_text = " ".join(paragraphs)

#IBM-specific cleanup:
#Remove author and promotional text after the article.
ending = (
    "Some level of human monitoring is recommended "
    "for such high-risk domains."
)

if ending in article_text:
    article_text = article_text.split(ending, 1)[0] + ending
else:
    print("WARNING: Expected article ending not found.")



#Update shared dataset without duplicates

output_dir = Path(__file__).resolve().parent.parent / "data"
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "scraped_articles.csv"

records = []

if output_file.exists():
    with open(
        output_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)
        records = list(reader)


records = [
    row for row in records
    if row.get("url") != URL
]

records.append({
    "url": URL,
    "title": title_text,
    "article_text": article_text
})

#Save all articles
with open(
    output_file,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["url", "title", "article_text"]
    )
    writer.writeheader()
    writer.writerows(records)

print("\nDataset updated!")
print("Total articles:", len(records))
print("IBM words:", len(article_text.split()))
print("Saved to:", output_file)

