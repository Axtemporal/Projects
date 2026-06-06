# FRED Macro Data Retriever

A reusable Python wrapper for the St. Louis Fed FRED API, built to retrieve and visualize U.S. macroeconomic time series.

---

## The Problem

Macro data — inflation, interest rates, economic uncertainty — is essential context for any equity or fixed income analysis. The FRED database hosts over 800,000 economic series, but querying it directly requires building API calls from scratch each time. This tool wraps that logic into reusable functions and applies them to three key series used in investment research.

---

## How It Works

### Core functions

**`get_FRED()`** — queries the FRED REST API for a single data series and returns a clean pandas DataFrame. Accepts series ID, date range, and output format as parameters.

**`compile_FRED()`** — takes a list of series names and IDs, calls `get_FRED()` for each, and merges them into a single DataFrame joined on observation dates. This makes it easy to build multi-variable macro datasets in one call.

### Series retrieved

| Script | FRED Series ID | Data |
|--------|---------------|------|
| US CPI Extractor | `CPIAUCSL` | Consumer Price Index, monthly (2016–2021) |
| Interest Rate Extractor | `DFF` | Federal Funds Effective Rate, daily (2017–2022) |
| Uncertainty Index | `GEPUCURRENT` | Global Economic Policy Uncertainty Index |

### Output
Each script computes the relevant metric (e.g. month-over-month CPI inflation rate), formats the date index, and plots the time series using Seaborn.

---

## Outputs

| Script | Output |
|--------|--------|
| CPI Extractor | Month-over-month U.S. inflation rate chart (2016–2021) |
| Interest Rate Extractor | Fed Funds Rate time series (2017–2022) |
| Uncertainty Index | Global Economic Policy Uncertainty Index chart |

---

## Technologies

| Package | Use |
|---------|-----|
| `urllib` / `json` | Direct FRED API calls |
| `pandas` | Data structuring and merging |
| `Seaborn` / `Matplotlib` | Time series visualization |

---

## How to Run

Replace `'XXXX'` in the `get_FRED()` call with your free FRED API key, available at [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html).

```bash
pip install pandas matplotlib seaborn
python "Inflação Estados Unidos CPI Extração FRED"
```

To retrieve a different series, change the `series_ids` list to any valid FRED series ID.
