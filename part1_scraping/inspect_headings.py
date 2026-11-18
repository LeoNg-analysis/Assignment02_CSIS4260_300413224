
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

URL = "https://www.ibm.com/think/topics/ai-agents"
USER_AGENT = "CSIS4260StudentResearchBot"

robots = RobotFileParser()
robots.set_url("https://www.ibm.com/robots.txt")
robots.read()

if not robots.can_fetch(USER_AGENT, URL):
    raise SystemExit("URL disallowed by robots.txt")

response = requests.get(
    URL,
    headers={"User-Agent": USER_AGENT},
    timeout=20
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("\nALL HEADINGS IN DOCUMENT ORDER:\n")

for i, heading in enumerate(
    soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]),
    start=1
):
    text = heading.get_text(" ", strip=True)

    if text:
        print(f"{i}. [{heading.name}] {text[:120]}")
