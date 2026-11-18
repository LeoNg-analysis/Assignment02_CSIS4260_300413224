
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

URL = "https://www.ibm.com/think/topics/ai-agents"
USER_AGENT = "CSIS4260StudentResearchBot"

robots = RobotFileParser()
robots.set_url("https://www.ibm.com/robots.txt")
robots.read()

if not robots.can_fetch(USER_AGENT, URL):
    raise SystemExit("URL is disallowed by robots.txt")

response = requests.get(
    URL,
    headers={"User-Agent": USER_AGENT},
    timeout=20
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

for tag in soup.find_all(["article", "main"]):
    print("\nCONTAINER:", tag.name)
    print("ID:", tag.get("id"))
    print("CLASS:", tag.get("class"))
    print("PARAGRAPHS:", len(tag.find_all("p")))

print("\nFOOTNOTES PARENT STRUCTURE:")

heading = soup.find(
    lambda tag: tag.name in ["h2", "h3", "h4", "h5", "h6"]
    and tag.get_text(" ", strip=True).lower() == "footnotes"
)

if heading:
    for parent in list(heading.parents)[:5]:
        print(
            "TAG:", parent.name,
            "| ID:", parent.get("id"),
            "| CLASS:", parent.get("class")
        )

print("\nPROMOTIONAL CONTENT SAMPLE:")

promo = soup.find(
    string=lambda text: text
    and "Build the future of your business" in text
)

if promo:
    for parent in list(promo.parents)[:5]:
        print(
            "TAG:", parent.name,
            "| CLASS:", parent.get("class")
        )

print("\nPROMOTIONAL PARAGRAPH ANCESTORS:")

for p in soup.find_all("p"):
    text = p.get_text(" ", strip=True)

    if "Build the future of your business" in text:
        print("\nTEXT:", text[:200])

        for parent in list(p.parents)[:12]:
            print(
                "TAG:", parent.name,
                "| CLASS:", parent.get("class"),
                "| ID:", parent.get("id")
            )
