
import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

USER_AGENT = "CSIS4260StudentResearchBot"

sources = {
    "IBM Think": "https://www.ibm.com/think/",
    "TechCrunch": "https://techcrunch.com/",
    "VentureBeat": "https://venturebeat.com/"
}

def check_source(name, url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    print(f"\nChecking: {name}")
    print(f"Robots URL: {robots_url}")

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=15
        )

        print(f"HTTP Status: {response.status_code}")

        if response.status_code != 200:
            print("Result: REVIEW REQUIRED")
            return

        parser = RobotFileParser()
        parser.parse(response.text.splitlines())

        allowed = parser.can_fetch(USER_AGENT, url)
        delay = parser.crawl_delay(USER_AGENT)

        print(f"Robots permission: {allowed}")
        print(f"Crawl delay: {delay}")

        if allowed:
            print("Result: ROBOTS ALLOWED - verify article URLs and terms")
        else:
            print("Result: NOT ALLOWED for this URL")

    except requests.RequestException as error:
        print(f"Result: ERROR - {error}")

for name, url in sources.items():
    check_source(name, url)
