# NLP Evaluation and Limitations

## 1. Evaluation Overview

This project applied four NLP techniques to a dataset of 50 articles about AI agents: TF-IDF keyword extraction, VADER sentiment analysis, rule-based business theme classification, and TextRank summarization enhanced with Maximal Marginal Relevance (MMR).

Evaluation focused on interpreting the outputs, manually reviewing selected results, and identifying limitations that could affect the reliability of the findings.

## 2. TF-IDF Keyword Extraction

TF-IDF was used to identify important words and phrases within the article collection. The model included unigrams and bigrams to capture individual terms and short phrases.

The resulting keywords provided a basis for exploring the main topics discussed across the articles.

However, TF-IDF measures statistical importance rather than semantic meaning. Common technical terms may receive high scores without necessarily representing the main argument of an article.

No formal keyword precision or recall evaluation was conducted.

## 3. VADER Sentiment Analysis

VADER classified 49 articles as positive and 1 as neutral, with an average compound score of 0.2349.

These results suggest that the selected articles generally contained positive language according to VADER.

However, VADER was originally designed for general sentiment analysis and may not accurately interpret specialized business and technical discussions.

For example, an article discussing the benefits of AI agents alongside security risks may still receive an overall positive sentiment score.

No manually labeled sentiment benchmark was used, so classification accuracy cannot be established from the observed distribution.

## 4. Rule-Based Theme Classification

A keyword-based classification approach was developed to identify 14 business themes across three categories: applications, benefits, and challenges.

An initial manual review examined 28 selected theme matches. Of these, 20 were marked correct, 5 incorrect, and 3 required further review.

Among the 25 matches receiving a definite correct or incorrect judgment, the observed precision was 80%.

This result represents a limited manual sample rather than the overall precision or accuracy of the classification system.

Following this review, selected challenge-related keyword rules were refined to reduce false positives.

However, the revised rules were not evaluated against a new labeled sample. Therefore, improvements in precision or recall cannot be confirmed.

The method may also miss relevant discussions expressed through synonyms, indirect language, or context-dependent terminology.

## 5. TextRank and MMR Summarization

TextRank was used to select important sentences from each article based on sentence similarity and graph-based ranking.

MMR was subsequently introduced to balance sentence importance with information diversity.

A qualitative comparison of selected summaries suggested that MMR reduced repetitive information in some cases.

For example, summaries concerning AI agent access permissions and low-quality AI-generated content showed less repetition after applying MMR.

Nevertheless, several limitations remained:

- Some extracted sentences contained section headings or numbered fragments.
- Certain quotations lacked sufficient surrounding context.
- Selected sentences did not always capture the central argument of an article.
- TF-IDF cosine similarity could not reliably detect all semantically redundant sentences.

A preliminary readability review of 10 summaries produced an average score of 3.3/5 before sentence-segmentation changes and 3.8/5 afterward.

These scores were based on informal manual judgments and should not be interpreted as a validated improvement attributable to MMR.

No reference-summary benchmark or formal ROUGE evaluation was conducted.

## 6. Dataset Limitations

The dataset consisted of 50 selected online articles published between 2024 and 2026.

The articles were collected from accessible online sources and filtered for relevance and publication information.

The dataset was not a random or representative sample of all publications about AI agents.

Source selection, article availability, publication bias, and differences in article length may influence the results.

Furthermore, the observed frequencies represent themes detected in articles rather than measured business outcomes or industry-wide adoption rates.

## 7. Recommendations for Future Improvement

Future work could improve the analysis by developing a larger manually annotated evaluation dataset, measuring precision and recall for each theme, and comparing rule-based classification with supervised or embedding-based approaches.

Sentiment analysis could be evaluated using human-labeled business and technology articles.

Summarization could be improved through more robust sentence segmentation, quotation handling, and evaluation against human-written reference summaries.

These improvements would help determine whether the observed NLP patterns remain consistent under more rigorous evaluation.
