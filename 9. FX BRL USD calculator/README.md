# FX Currency Converter

Real-time currency converter powered by the Frankfurter API.

---

## The Problem

Quick currency conversions with live rates — without relying on a browser, spreadsheet, or paid data feed. This tool fetches the current exchange rate from a free public API and converts any amount between any two currencies in seconds.

---

## How It Works

1. **API call** — sends a GET request to [frankfurter.app](https://www.frankfurter.app), a free, registration-free service that sources rates from the European Central Bank
2. **Rate extraction** — parses the JSON response to extract the converted value and implied exchange rate
3. **Output** — prints the converted amount and the spot rate for the currency pair

---

## Example Output

```
  100.00 USD = 512.35 BRL
  Exchange rate: 1 USD = 5.1235 BRL
```

---

## Configuration

Edit the three variables at the top of the script:

| Variable | Description | Example |
|----------|-------------|---------|
| `moeda_origem` | Source currency (ISO 4217) | `"USD"` |
| `moeda_destino` | Target currency (ISO 4217) | `"BRL"` |
| `valor` | Amount to convert | `100` |

Supports any currency pair available on the ECB feed (EUR, USD, BRL, GBP, JPY, and 30+ others).

---

## Technologies

| Package | Use |
|---------|-----|
| `requests` | HTTP GET to Frankfurter API |
| `json` | Response parsing |

---

## How to Run

```bash
pip install requests
python "Operador de Câmbio API.py"
```
