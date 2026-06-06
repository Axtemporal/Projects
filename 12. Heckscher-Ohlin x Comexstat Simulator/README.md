# Heckscher-Ohlin × Comexstat Simulator

Tests Heckscher-Ohlin trade theory predictions against real Brazilian bilateral trade data from the ComexStat API.

---

## The Problem

The Heckscher-Ohlin (H-O) theorem predicts that countries export goods that use their abundant factors of production intensively. Brazil, as a resource-rich and labor-abundant economy, should export labor-intensive and natural-resource goods while importing capital-intensive ones. This tool tests that prediction empirically using official trade statistics, classifying Brazil's entire export and import basket by factor intensity for any two trading partners.

---

## How It Works

### Part 1 — Commodity-level data collection
Queries the ComexStat API for a user-defined product (NCM code) and date range, generating the same 6-panel trade dashboard as [Project 2](../2.%20Brazil%20Export%20Import%20Data%20Retriever%20-%20Comexstat): FOB value, volume, implicit price, trade balance, and top trading partners.

### Part 2 — Bilateral factor intensity analysis

**Step 1 — NCM classification**
Each NCM chapter (2-digit prefix) is classified into one of three factor categories based on trade economics literature (Lall 2000, Krugman & Obstfeld 2018):

| Category | NCM Chapters |
|----------|-------------|
| **Capital-intensive** | Chemicals, plastics, metals, machinery, electronics, vehicles, instruments (caps. 28–40, 72–93) |
| **Labor-intensive** | Agriculture, food, textiles, apparel, footwear, wood, paper, furniture (caps. 1–24, 44–67, 94–96) |
| **Others** | Minerals, fuels, leather, precious stones, art |

**Step 2 — Bilateral data retrieval**
Fetches the full trade basket (imports and exports) between Brazil and two configurable partner countries (default: China and USA) — either restricted to selected NCMs or across the entire trade agenda.

**Step 3 — H-O reading**
For each bilateral pair, the tool computes the capital/labor composition of imports and exports and prints an H-O interpretation:
- What factor intensity does Brazil import from each partner?
- What factor intensity does Brazil export to each partner?
- Does the pattern confirm the H-O prediction?

### Part 3 — Bilateral dashboard (6 panels)

| Panel | Content |
|-------|---------|
| Imports by factor intensity | Capital vs. labor-intensive imports, Partner A vs. B |
| Exports by factor intensity | Capital vs. labor-intensive exports, Partner A vs. B |
| Monthly import series | Bilateral import evolution over time |
| Monthly export series | Bilateral export evolution over time |
| Import composition (%) | Stacked bar: share of each factor category |
| Export composition (%) | Stacked bar: share of each factor category |

---

## Outputs

- Console H-O interpretation for each bilateral pair
- `comexstat_dashboard.png` — commodity-level 6-panel dashboard
- `comexstat_bilateral.png` — bilateral factor intensity 6-panel dashboard

---

## Technologies

| Package | Use |
|---------|-----|
| `requests` | ComexStat API calls with retry/backoff |
| `pandas` | Data processing and merging |
| `NumPy` | Array operations for stacked charts |
| `Matplotlib` | Both dashboards |

---

## How to Run

```bash
pip install requests pandas numpy matplotlib
python "Economia Monetária - Heckscher-Ohlin x comexstat API.py"
```

Configure `PAIS_A`, `PAIS_B`, `NCM_CODES`, and the year range at the top of the script. Use `listar_paises_e_codigos()` to look up MDIC country codes.
