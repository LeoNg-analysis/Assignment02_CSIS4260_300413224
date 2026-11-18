
from urllib.robotparser import RobotFileParser

url = "https://kpmg.com/us/en/articles/2025/ai-agents-shaping-talent-strategy.html"
user_agent = "CSIS4260StudentResearchBot"

robots = RobotFileParser()
robots.set_url("https://kpmg.com/robots.txt")

try:
    robots.read()

    print("Robots URL:", robots.url)
    print("Allowed:", robots.can_fetch(user_agent, url))
    print("Crawl delay:", robots.crawl_delay(user_agent))

except Exception as error:
    print("Could not verify robots.txt:", error)
