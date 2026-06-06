# S&P 500 Volatility Study — GARCH(1,1)

Conditional volatility estimation for S&P 500 daily returns using ARCH and GARCH models.

---

## The Problem

Stock return volatility is not constant — it clusters: volatile periods tend to follow volatile periods, and calm periods tend to follow calm ones. Standard deviation over a fixed window misses this dynamic. GARCH models solve this by estimating a time-varying conditional variance, which is the foundation of modern risk management and options pricing.

---

## How It Works

### Part 1 — ARCH(1) simulation
Before applying the model to real data, the code simulates an ARCH(1) process from scratch to illustrate the mechanics:
- Parameters: α₀ = 0.1, α₁ = 0.8, T = 1,000 periods
- Shows how shocks propagate into future variance
- Plots both the simulated return series εₜ and the conditional variance hₜ

### Part 2 — Real S&P 500 data
1. Downloads S&P 500 daily prices for 2018 from the FRED API (`SP500` series)
2. Computes daily logarithmic returns: log(Pₜ / Pₜ₋₁)
3. Calculates a 20-day rolling historical volatility as a baseline benchmark

### Part 3 — GARCH(1,1) estimation
1. Fits a GARCH(1,1) model with constant mean to log-returns scaled to percentage points
2. Extracts the conditional volatility series estimated by the model
3. Plots GARCH-estimated volatility against the 20-day rolling baseline

### Part 4 — Diagnostic tests
| Test | Purpose |
|------|---------|
| Standardized residuals plot | Check for remaining structure in residuals |
| ACF of residuals | Test for autocorrelation in standardized residuals |
| ACF of residuals² | Test for remaining ARCH effects |
| Q-Q plot | Check normality assumption of residuals |
| Ljung-Box test (lag 10) | Formal test for autocorrelation in squared residuals |

---

## Outputs

| Output | Description |
|--------|-------------|
| ARCH(1) simulation | εₜ series and conditional variance hₜ |
| S&P 500 log returns | Daily return chart for 2018 |
| Rolling volatility | 20-day historical volatility baseline |
| GARCH vs. historical | Conditional volatility comparison chart |
| Residual diagnostics | ACF, ACF², Q-Q plot, standardized residuals |
| Model summary | GARCH(1,1) parameter estimates and Ljung-Box test |

---

## Technologies

| Package | Use |
|---------|-----|
| `arch` | GARCH(1,1) model estimation |
| `statsmodels` | ACF plots, Q-Q analysis, Ljung-Box test |
| `pandas_datareader` | S&P 500 price data from FRED API |
| `NumPy` / `pandas` | Log return and variance calculations |
| `Matplotlib` | All charts |

---

## How to Run

```bash
pip install arch pandas_datareader statsmodels numpy pandas matplotlib
python sp500_garch_model.py
```
