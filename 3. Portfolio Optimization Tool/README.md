# Portfolio Optimization Tool

Markowitz mean-variance portfolio optimizer for Brazilian equities, built with Monte Carlo simulation.

---

## The Problem

Choosing how to split capital across multiple stocks is not intuitive. Simply picking the stock with the best past return ignores risk. This tool formalizes the decision: given a set of B3-listed equities, it finds the allocation that delivers the best risk-adjusted return — measured by the Sharpe ratio.

---

## How It Works

### 1. Ticker input and validation
The user enters B3 tickers one at a time. Each ticker is validated against a live list from Investing.com before being added to the portfolio.

### 2. Price data collection
Adjusted closing prices are downloaded from Yahoo Finance via `yfinance`, starting from January 2020 through the current date.

### 3. Performance history
All prices are normalized to 1 on the start date, making returns directly comparable across stocks. The best performer is highlighted in blue on the chart.

### 4. Risk vs. Return analysis
Annualized return (mean × 252) and volatility (std × √252) are calculated for each stock and plotted on a scatter chart — the same framework used in CFA-level portfolio theory.

### 5. Monte Carlo simulation — 100,000 portfolios
Random portfolio weights are generated 100,000 times. For each simulated portfolio, the tool calculates:
- Annualized return
- Annualized volatility
- Sharpe ratio
- 5th percentile daily return (Value at Risk proxy)

### 6. Optimal allocation
The portfolio with the highest Sharpe ratio is selected. The efficient frontier is plotted with a Sharpe-based color scale, and the optimal point is marked in blue.

### 7. Recommended weights
A pie chart displays the recommended allocation across the selected stocks.

### 8. QuantStats performance reports
For each stock of interest, the tool generates a full HTML performance report benchmarked against the Ibovespa index, including:
- Cumulative returns vs. benchmark
- Rolling Sharpe, Sortino, and Beta (6-month windows)
- Worst drawdown periods
- Monthly active returns heatmap
- Return quantile distribution

---

## Outputs

| Output | Description |
|--------|-------------|
| Normalized price chart | Cumulative performance since Jan 2020, best performer highlighted |
| Risk vs. Return scatter | Annualized risk and return per stock |
| Efficient frontier | 100,000 simulated portfolios, color-coded by Sharpe ratio |
| Allocation pie chart | Recommended portfolio weights |
| HTML reports | Full QuantStats report per stock vs. Ibovespa |

---

## Technologies

| Package | Use |
|---------|-----|
| `yfinance` | Historical adjusted price data |
| `investpy` | B3 ticker validation |
| `NumPy` / `pandas` | Return and risk calculations |
| `Matplotlib` / `Seaborn` | Static charts |
| `QuantStats` | Full performance reporting |

---

## How to Run

```bash
pip install pandas numpy yfinance seaborn matplotlib quantstats investpy
python portfolio_optimizer.py
```

When prompted, enter B3 tickers one at a time (e.g. `PETR4`, `VALE3`). Type `pare` to stop.
