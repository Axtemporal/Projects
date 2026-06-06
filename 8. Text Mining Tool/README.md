# Text Mining Tool

A lightweight NLP pipeline for frequency analysis, sentiment scoring, and word cloud generation from unstructured text.

---

## The Problem

Large volumes of unstructured text — customer reviews, earnings call transcripts, news articles — contain signals that are hard to quantify manually. This tool applies a standard text mining pipeline to extract word frequency patterns, classify sentiment, and identify dominant themes in any input text.

---

## How It Works

### Step 1 — Preprocessing
Cleans and normalizes raw text through four operations:
1. Convert to lowercase
2. Remove punctuation
3. Filter stopwords (custom Portuguese stopword list)
4. Tokenize (split into individual words)

### Step 2 — Word Frequency Analysis
Counts occurrences of each token after preprocessing using `Counter`. Reports the top 10 most frequent words.

### Step 3 — Sentiment Classification
Classifies each token against two pre-defined word lists:
- **Positive words**: excelente, bom, satisfeito, rápida, ótimo, perfeito
- **Negative words**: ruim, defeito, atraso, demorada, péssimo, problema

Computes a sentiment score:

```
Sentiment = (N_positive − N_negative) / Total tokens
```

A positive score indicates net positive sentiment; negative score indicates net negative.

### Step 4 — Theme Categorization
Groups negative signals into two categories — **product** and **delivery** — and identifies which is the dominant source of complaints.

### Word Cloud
Generates a visual word cloud from the cleaned token list, sized by frequency.

---

## Outputs

| Output | Description |
|--------|-------------|
| Word cloud chart | Visual frequency map of tokens |
| Top 10 words | Ranked list of most frequent terms |
| Sentiment score | Numeric score with positive/negative/neutral label |
| Theme analysis | Product vs. delivery problem breakdown |

---

## Technologies

| Package | Use |
|---------|-----|
| `wordcloud` | Word cloud generation |
| `collections.Counter` | Word frequency counting |
| `Matplotlib` | Chart display |

---

## How to Run

```bash
pip install wordcloud matplotlib
python "Business Inteligence - Text Mining - 2026.1 IBMEC Rio.py"
```

Replace the `texto` variable with any input text to analyze.
