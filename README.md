# CSIS4260 – Assignment 2: Web Scraping and NLP Analysis

## The Business Value of AI Agents

**Research Question:** How can AI agents create value for businesses, and what benefits, applications, and challenges are highlighted in online articles?

## 1. Project Overview

This project investigates how AI agents are discussed in business and technology publications, focusing on potential benefits, business applications, and adoption challenges.

The analysis combines web scraping, text preprocessing, natural language processing (NLP), and exploratory data analysis.

The final dataset contains 50 articles published between 2024 and 2026.

## 2. Project Structure

````text
Assignment02_CSIS4260_300413224/
Assignment02_CSIS4260_300413224/
├── data/
│   ├── nlp_articles.csv
│   ├── preprocessed_articles.csv
│   ├── tfidf_keywords.csv
│   ├── sentiment_results.csv
│   ├── business_themes.csv
│   ├── textrank_summaries.csv
│   └── final_nlp_results.csv
├── part1_scraping/
│   ├── bulk_scraper.py
│   ├── benchmark.py
│   └── relevance_filter.py
├── part2_nlp/
│   ├── text_preprocessing.py
│   ├── tfidf_analysis.py
│   ├── vader_sentiment.py
│   ├── business_theme_classification.py
│   └── textrank_summarization.py
├── part3_analysis/
│   ├── combine_nlp_results.py
│   ├── exploratory_analysis.py
│   ├── create_visualizations.py
│   ├── findings_discussion.md
│   ├── nlp_evaluation.md
│   └── figures/
├── check_environment.py
├── requirements.txt
└── README.md

_The directory listing above shows the main files. Additional scraping, verification, auditing, and validation scripts are included in the repository._

## 3. Data Collection

Articles were collected from online business and technology publications, including IBM, Microsoft, MIT-related publications, KPMG, and other sources.

The scraping workflow involved identifying candidate URLs, extracting article text, reviewing article relevance, removing duplicate records, and verifying publication dates.

The initial scraped dataset contained 63 articles. After cleaning and relevance filtering, 53 unique articles remained. The final NLP dataset included 50 articles with verified publication information.

## 4. NLP Methodology

### 4.1 Text Preprocessing

Article text was cleaned and prepared for NLP analysis. The preprocessing workflow reduced unnecessary text and standardized content for keyword extraction.

The original article text was retained for sentiment analysis and extractive summarization.

### 4.2 TF-IDF Keyword Extraction

TF-IDF was applied to identify important words and phrases within the article collection.

The model used unigrams and bigrams, English stop-word filtering, and a maximum of 5,000 features.

The results were saved to `data/tfidf_keywords.csv`.

### 4.3 VADER Sentiment Analysis

VADER was used to analyze the sentiment of article sentences.

Sentence-level compound scores were aggregated to produce article-level sentiment scores and labels.

Results were saved to `data/sentiment_results.csv`.

### 4.4 Business Theme Classification

A rule-based keyword classification method identified 14 business themes across three categories:

- Applications: operations, customer service, marketing, sales, and data analytics.
- Benefits: automation, productivity, cost efficiency, and decision-making.
- Challenges: security, human oversight, reliability, integration, and cost.

The results were saved to `data/business_themes.csv`.

### 4.5 TextRank and MMR Summarization

TextRank was used to identify important sentences through TF-IDF cosine similarity and graph-based PageRank.

Maximal Marginal Relevance (MMR) was introduced to balance sentence importance with information diversity.

Extractive summaries were saved to `data/textrank_summaries.csv`.

## 5. Key Findings

The analysis identified the following patterns across 50 articles:

| Theme            | Articles | Percentage |
| ---------------- | -------: | ---------: |
| Automation       |       45 |        90% |
| Productivity     |       45 |        90% |
| Operations       |       40 |        80% |
| Security         |       30 |        60% |
| Customer Service |       27 |        54% |
| Human Oversight  |       22 |        44% |

VADER classified 49 articles as positive and 1 as neutral, with an average compound score of 0.2349.

These results describe patterns detected in the selected articles. They do not measure actual business performance, adoption rates, or causal effects.

Detailed findings are available in `part3_analysis/findings_discussion.md`.

## 6. Evaluation and Limitations

An initial manual review of business theme matches produced 20 correct classifications, 5 incorrect classifications, and 3 requiring further review.

The observed precision among the 25 definitively reviewed matches was 80%. This result is limited to the reviewed sample and does not establish overall model accuracy.

A preliminary manual readability comparison of 10 TextRank summaries produced average scores of 3.3/5 before sentence-segmentation changes and 3.8/5 afterward.

These informal scores do not establish a statistically validated improvement.

Other limitations include the small and nonrepresentative article sample, keyword-dependent classification, potential sentiment misinterpretation, and context loss in extractive summarization.

See `part3_analysis/nlp_evaluation.md` for further discussion.

## 7. Installation and Execution

### Requirements

- Python 3
- Dependencies listed in `requirements.txt`

### Create a Virtual Environment

```bash
python -m venv .venv
````

Activate it on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Run NLP Analysis

The following commands assume that the corresponding input CSV files already exist in the `data/` directory.

```bash
python part2_nlp/text_preprocessing.py
python part2_nlp/tfidf_analysis.py
python part2_nlp/vader_sentiment.py
python part2_nlp/business_theme_classification.py
python part2_nlp/textrank_summarization.py
```

### Combine Results

```bash
python part3_analysis/combine_nlp_results.py
```

### Exploratory Data Analysis

```bash
python part3_analysis/exploratory_analysis.py
```

### Generate Visualizations

```bash
python part3_analysis/create_visualizations.py
```

Generated figures are saved to `part3_analysis/figures/`.

## 8. Main Outputs

- `data/final_nlp_results.csv` – Combined article-level NLP results.
- `data/tfidf_keywords.csv` – TF-IDF keyword scores.
- `data/sentiment_results.csv` – VADER sentiment results.
- `data/business_themes.csv` – Business theme detection results.
- `data/textrank_summaries.csv` – Extractive summaries.
- `part3_analysis/figures/` – Data visualizations.
- `part3_analysis/findings_discussion.md` – Research findings.
- `part3_analysis/nlp_evaluation.md` – Evaluation and limitations.

## 9. Conclusion

The analysis suggests that automation, productivity, and operational applications are prominent themes in online discussions about AI agents.

Security and human oversight are also frequently discussed, indicating that potential business benefits are accompanied by implementation and governance concerns.

The project demonstrates how web scraping and multiple NLP techniques can be combined to extract and analyze patterns from online articles.
