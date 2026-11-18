
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

USER_AGENT = "CSIS4260StudentResearchBot"

url = "https://www.ibm.com/think/topics/ai-agents"

robots = RobotFileParser()
robots.set_url("https://www.ibm.com/robots.txt")
robots.read()

if not robots.can_fetch(USER_AGENT, url):
    print("Robots.txt does not allow this URL.")
    raise SystemExit(1)

headers = {"User-Agent": USER_AGENT}

response = requests.get(
    url,
    headers=headers,
    timeout=20
)

print("HTTP Status:", response.status_code)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

title = soup.find("h1")
paragraphs = soup.find_all("p")

print("\nTITLE:")
print(title.get_text(" ", strip=True) if title else "Not found")

print("\nPARAGRAPHS FOUND:", len(paragraphs))

print("\nTEXT PREVIEW:")
for p in paragraphs[:5]:
    print(p.get_text(" ", strip=True))
