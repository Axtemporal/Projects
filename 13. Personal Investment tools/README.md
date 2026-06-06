# Monthly Contribution Simulator

Simulates long-term wealth accumulation under compound interest, with inflation adjustment to show real purchasing power.

---

## The Problem

Compound interest projections often report only nominal figures — the raw account balance — without accounting for inflation. This tool calculates both the nominal and real (inflation-adjusted) portfolio trajectory, making clear how much of the final balance represents actual purchasing power versus monetary inflation.

---

## How It Works

### Rate conversion
Annual interest and inflation rates are converted to monthly equivalents using the exact compound formula:

```
monthly_rate = (1 + annual_rate / 100) ^ (1/12) − 1
```

### Month-by-month simulation
For each month in the simulation period:
1. Applies compound interest to the current balance
2. Adds the monthly contribution
3. Computes the real value by deflating the nominal balance by the accumulated inflation factor: `nominal / (1 + monthly_inflation)^month`
4. Records nominal balance, real balance, and total amount contributed (without returns)

### Output
Prints a full results summary and generates a 3-line chart:

| Line | Description |
|------|-------------|
| **Nominal wealth** (blue) | Raw portfolio balance including inflation |
| **Real wealth** (green, dashed) | Inflation-adjusted purchasing power |
| **Total contributed** (grey, dotted) | Sum of deposits with no returns |

The area between the nominal line and total contributed is shaded to highlight interest earned.

---

## Example (default parameters)

| Parameter | Value |
|-----------|-------|
| Initial capital | R$ 5,000 |
| Monthly contribution | R$ 1,000 |
| Annual interest rate | 12% |
| Estimated annual inflation | 4.5% |
| Simulation period | 10 years |

---

## Technologies

| Package | Use |
|---------|-----|
| `Matplotlib` | Line chart with shaded interest area |
| `matplotlib.ticker` | BRL currency formatting on y-axis |

---

## How to Run

```bash
pip install matplotlib
python "Simulador aportes mensais - matplotlib.py"
```

Edit the parameters at the top of the script to match your own scenario.
