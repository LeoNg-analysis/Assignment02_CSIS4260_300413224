
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

URL = (
    "https://kpmg.com/us/en/articles/2025/"
    "ai-agents-shaping-talent-strategy.html"
)

USER_AGENT = "CSIS4260StudentResearchBot"

robots = RobotFileParser()
robots.set_url("https://kpmg.com/robots.txt")
robots.read()

if not robots.can_fetch(USER_AGENT, URL):
    raise SystemExit("Scraping not allowed.")

response = requests.get(
    URL,
    headers={"User-Agent": USER_AGENT},
    timeout=20
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("\nPAGE TITLE:")
print(soup.title.get_text(" ", strip=True) if soup.title else "")

print("\nMAIN / ARTICLE ELEMENTS:")

for tag in soup.find_all(["main", "article"]):
    print(
        "TAG:", tag.name,
        "| ID:", tag.get("id"),
        "| CLASS:", tag.get("class"),
        "| PARAGRAPHS:", len(tag.find_all("p"))
    )

print("\nH1 AND H2 HEADINGS:")

for heading in soup.find_all(["h1", "h2"]):
    print(
        f"[{heading.name}]",
        heading.get_text(" ", strip=True)[:150]
    )
