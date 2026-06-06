# B3 Performance Dashboard

Interactive dashboard for monitoring Ibovespa index price performance and trading volume.

---

## The Problem

Tracking index performance over custom time windows — with price and volume in the same view — typically requires a Bloomberg terminal or manual work in Excel. This tool pulls live data and renders an interactive dashboard in seconds, directly in Python.

---

## How It Works

1. **Data collection** — downloads Ibovespa (`^BVSP`) OHLCV data from Yahoo Finance via `yfinance` for a defined date range
2. **Price chart** — line chart of daily closing prices plotted on the left y-axis
3. **Volume chart** — bar chart of daily trading volume plotted on the right y-axis
4. **Combined dashboard** — both series overlaid on a single interactive Plotly figure with independent dual y-axes, allowing zooming, panning, and hovering for exact values on any day

---

## Outputs

An interactive Plotly dashboard displaying:
- Ibovespa closing price over the selected period
- Daily trading volume as bars on a secondary axis
- Hover tooltips with exact date, price, and volume

---

## Technologies

| Package | Use |
|---------|-----|
| `yfinance` | Ibovespa historical OHLCV data |
| `Plotly` | Interactive dual-axis dashboard |
| `pandas` | Data handling |

---

## How to Run

```bash
pip install yfinance plotly pandas
python "B3 performance Monitor.py"
```

To change the date range, edit the `start_date` and `end_date` variables at the top of the script.
