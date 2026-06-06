# ANP O&G BI Scrapper

Automated scraper for Brazil's National Petroleum Agency (ANP) Power BI production dashboard.

---

## The Problem

The ANP publishes oil and gas production data on a Power BI dashboard — interactive, but not downloadable directly. Extracting this data manually requires navigating multiple pages and copying tables. This tool automates the entire process, navigating the dashboard programmatically and exporting all data to structured files.

---

## How It Works

1. **Browser automation** — launches a Chromium browser via Playwright and navigates to the ANP's public Power BI panel
2. **Page mapping** — scans the dashboard's index page and lists all visible navigation links
3. **Page navigation** — clicks into each target page (configurable list: "Total", "Agregada", "Tabela Produção")
4. **Data capture** — extracts all visible text from Power BI visual containers: KPI cards, table cells, and chart labels
5. **Table scrolling** — for paginated tables, scrolls the virtual container incrementally to capture all rows beyond the initial viewport
6. **Screenshots** — saves a screenshot of each page visited for visual reference
7. **Export** — saves all captured data as:
   - A single `dados.json` with all results organized by page and selector
   - Individual `.csv` files per data section

---

## Outputs

| File | Description |
|------|-------------|
| `00_indice.png` | Screenshot of the dashboard index |
| `01_Total.png`, `02_Agregada.png`, etc. | Screenshots of each visited page |
| `dados.json` | All extracted data in structured JSON |
| `*.csv` | One CSV per data section |

---

## Technologies

| Package | Use |
|---------|-----|
| `playwright` | Browser automation (Chromium) |
| `pandas` | Data structuring and CSV export |
| `json` | JSON serialization |

---

## How to Run

```bash
pip install playwright pandas
playwright install chromium
python anp_painel_scraper.py
```

To change which pages are scraped, edit the `PAGINAS_ALVO` list at the top of the script.
