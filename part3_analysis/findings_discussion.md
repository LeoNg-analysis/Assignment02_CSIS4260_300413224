# Findings and Discussion

## 1. Dataset Overview

The final dataset consists of 50 online articles published between 2024 and 2026, focusing on AI agents, their business applications, potential benefits, and adoption challenges. Of these articles, 3 were published in 2024, 25 in 2025, and 22 in 2026.

The dataset was analyzed using four natural language processing approaches: TF-IDF keyword extraction, VADER sentiment analysis, rule-based business theme classification, and TextRank summarization enhanced with Maximal Marginal Relevance (MMR).

## 2. Business Benefits of AI Agents

Automation and productivity were the most frequently detected benefits, each appearing in 45 out of 50 articles (90%).

These findings suggest that automation and productivity are central topics in online discussions about the business value of AI agents.

Cost efficiency was detected in 11 articles (22%), while decision-making appeared in 7 articles (14%). These lower frequencies may reflect differences in article focus and the coverage of the rule-based keyword dictionaries.

## 3. Business Applications

Operations was the most frequently identified application area, appearing in 40 articles (80%). Customer service followed with 27 articles (54%), marketing with 18 articles (36%), sales with 15 articles (30%), and data analytics with 10 articles (20%).

These findings indicate that the analyzed articles frequently associate AI agents with operational workflows and customer-facing activities.

However, theme frequency should not be interpreted as actual adoption rates across industries or organizations.

## 4. Adoption Challenges

Security was the most frequently detected challenge, appearing in 30 articles (60%), followed by human oversight in 22 articles (44%).

Reliability was identified in 9 articles (18%), integration in 6 articles (12%), and cost-related challenges in 4 articles (8%).

These findings highlight the importance of security and human supervision in discussions about AI agent deployment.

Because theme classification relied on predefined keyword rules, the observed frequencies are sensitive to the selected keywords and may not capture all relevant discussions.

## 5. Sentiment Analysis

VADER sentiment analysis classified 49 articles (98%) as positive and 1 article (2%) as neutral. The average compound score was 0.2349.

This indicates that the selected articles generally contained language classified as positive by VADER.

However, positive sentiment does not necessarily indicate that an article endorses AI agents or demonstrates positive business outcomes. VADER is a lexicon-based method and may not fully capture technical criticism, contextual meaning, or mixed evaluations.

## 6. Text Summarization

TextRank was applied to generate extractive summaries from the articles. Maximal Marginal Relevance (MMR) was subsequently introduced to reduce repetitive content and encourage diversity among selected sentences.

Qualitative inspection suggested that MMR reduced repeated ideas in some articles, particularly those discussing agent security and low-quality AI-generated work.

Nevertheless, limitations remained, including headings embedded in extracted sentences and quotations that lacked sufficient context.

## 7. Overall Discussion

The findings suggest that online discussions of AI agents emphasize automation, productivity, and operational applications, while also acknowledging security and human oversight challenges.

Together, these results provide a descriptive view of the opportunities and concerns associated with AI agents in business contexts.

The findings should be interpreted as patterns within the selected article dataset rather than evidence of causal business impact, measured productivity gains, or representative industry-wide adoption.
