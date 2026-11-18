
import pandas as pd

df = pd.read_csv("data/scraped_articles.csv")

print("Total articles:", len(df))
print("Columns:", df.columns.tolist())

for index, row in df.iterrows():
    text = str(row["article_text"])

    print("\nARTICLE:", row["title"])
    print("Word count:", len(text.split()))

    print("\nFIRST 500 CHARACTERS:")
    print(text[:500])

    print("\nLAST 500 CHARACTERS:")
    print(text[-500:])

from bs4 import BeautifulSoup
import requests

url = df.iloc[0]["url"]

response = requests.get(
    url,
    headers={"User-Agent": "CSIS4260StudentResearchBot"},
    timeout=20
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("\nPOSSIBLE REFERENCE HEADINGS:")

for heading in soup.find_all(
    ["h2", "h3", "h4", "h5", "h6"]
):
    heading_text = heading.get_text(" ", strip=True)

    if any(
        keyword in heading_text.lower()
        for keyword in [
            "reference",
            "citation",
            "footnote",
            "source"
        ]
    ):
        print(
            "Tag:", heading.name,
            "| Text:", heading_text,
            "| Parent class:",
            heading.parent.get("class")
            if heading.parent else None
        )
