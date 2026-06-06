# Daily News Clipping — B3 Sectors

Automated daily news aggregator for B3-listed companies, organized by sector and translated to English.

---

## The Problem

Equity research requires daily monitoring of news across multiple companies and sectors. Manually scanning Google News for each ticker is time-consuming. This tool automates the full pipeline: searches Google News RSS for each company and sector-level term, resolves links, translates headlines to English, and outputs a clean Word document ready to use as a morning briefing.

---

## How It Works

### 1. Search configuration
Each sector contains a list of search terms — typically company names + tickers (e.g., `"Petrobras" PETR4`) or sector-level topics (e.g., `preço petróleo Brent`). The search window defaults to the last 24 hours.

### 2. RSS feed collection
For each search term, the tool constructs a Google News RSS URL with Brazilian locale parameters (`pt-BR`, `BR`) and parses the feed using `feedparser`. Returns article title, source, publication date, and URL.

### 3. Link resolution
Google News RSS returns redirect URLs. The tool resolves each one to the actual article URL using parallel HTTP requests (`ThreadPoolExecutor`), making the links directly clickable in the output document.

### 4. Title translation
All headlines are translated from Portuguese to English using `GoogleTranslator` (deep-translator), also running in parallel for speed.

### 5. Word document generation
Outputs a `.docx` file organized hierarchically:
- **Heading 1**: Sector
- **Heading 2**: Search term
- **Bullet points**: `Article title (Source, Month DD)` — title is a hyperlink to the real article URL

---

## Sectors Covered

| Sector | Key names |
|--------|-----------|
| Oil & Gas | Petrobras, PRIO, Brava, PetroRecôncavo, Brent price, ANP |
| Metals & Mining | Vale, CSN Mineração, Gerdau, Usiminas, Aura, iron ore price |
| Fuel Distribution | Vibra, Raízen, Ultrapar, Cosan, RenovaBio |
| Natural Gas | Comgás, Compass, gas market reform |
| Agriculture | SLC, BrasilAgro, 3tentos, Boa Safra, soy/corn prices |
| Fertilizers | Heringer, Vittia, urea price |
| Petrochemicals | Braskem, Unipar, ethylene price |
| Paper & Pulp | Suzano, Klabin, Irani, Eucatex, BHKP pulp price |

---

## Output

A `.docx` file named `noticias_setoriais_YYYYMMDD.docx` saved in the script's directory, with all headlines hyperlinked and translated to English.

---

## Technologies

| Package | Use |
|---------|-----|
| `feedparser` | Google News RSS parsing |
| `requests` | Link resolution via HTTP HEAD/GET |
| `deep-translator` | Portuguese → English title translation |
| `python-docx` | Word document generation with hyperlinks |
| `concurrent.futures` | Parallel link resolution and translation |

---

## How to Run

```bash
pip install feedparser python-docx requests deep-translator
python news_rss_collector_B3_setorial.py
```

To add sectors or companies, edit the `SETORES` dictionary at the top of the script.
