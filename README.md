# 📈 Stock Market Dashboard

An interactive financial analysis dashboard built in Python. Fetches live market data, computes return and risk metrics from first principles, and presents everything through a Streamlit web interface.

> Built as a deliberate deep-dive into quantitative finance — every metric is implemented manually and understood before it is visualized.

---

## Dashboard

![Stock Dashboard Preview](Screenshot%202026-06-26%20at%2011.33.24%E2%80%AFPM.png)

---

## Features

✅ Live OHLCV data via Yahoo Finance API  
✅ Closing price, candlestick, and volume charts  
✅ Daily returns, cumulative returns, return distribution  
✅ Annualized volatility and 30-day rolling volatility  
✅ Company fundamentals — Market Cap, PE Ratio, Beta, Dividend Yield  
✅ Multi-stock comparison with normalized prices and risk/return scatter  
✅ CSV export for any ticker and period  

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.11 |
| Data | yfinance · pandas · numpy |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Environment | venv |

---

## Architecture

```
Yahoo Finance API
      ↓
data_loader.py    — fetch & clean OHLCV + fundamentals
      ↓
analysis.py       — returns, volatility, normalization, comparison
      ↓
visualization.py  — Plotly chart functions
      ↓
app.py            — Streamlit UI (no business logic)
```

`app.py` is a pure UI layer. All computation lives in `src/`. Each module has one responsibility and is independently reusable.

---

## Project Structure

```
stock-market-dashboard/
│
├── src/
│   ├── data_loader.py       # API calls, data fetching
│   ├── analysis.py          # All metric computation
│   ├── visualization.py     # All Plotly figures
│   └── utils.py             # Cleaning, formatting, summaries
│
├── data/                    # Downloaded CSVs (gitignored)
├── assets/                  # Screenshots and demo GIF
├── docs/                    # Finance concept deep-dives
├── app.py                   # Streamlit dashboard
├── main.py                  # Terminal runner
└── requirements.txt
```

---

## Setup

```bash
git clone https://github.com/rishu-sriv/stock-market-dashboard.git
cd stock-market-dashboard

python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
python -m streamlit run app.py
```

> Use `python -m streamlit` to ensure the venv's Streamlit is used over any system-level installation.

---

## Supported Markets

| Market | Suffix | Example |
|---|---|---|
| US (NASDAQ/NYSE) | _(none)_ | `AAPL`, `MSFT`, `TSLA` |
| India — NSE | `.NS` | `RELIANCE.NS`, `TCS.NS` |
| India — BSE | `.BO` | `INFY.BO`, `HDFCBANK.BO` |
| UK | `.L` | `HSBA.L`, `BP.L` |
| Germany | `.DE` | `SAP.DE`, `BMW.DE` |

---

## Finance Concepts Implemented

| Concept | Implementation |
|---|---|
| Adjusted Close | Used for all return calculations — accounts for splits and dividends |
| Daily Return | `pct_change()` on adjusted closing price |
| Cumulative Return | `(1 + r).cumprod()` — compounded multiplication, not summation |
| Annualized Volatility | `daily_std × √252` |
| Rolling Volatility | 30-day window, recalculated daily |
| Normalized Price | `(price / price[0]) × 100` — fair cross-stock comparison |
| Return/Risk Ratio | Total return ÷ annualized volatility (simplified Sharpe) |
| Beta | Market sensitivity from Yahoo Finance fundamentals |
| PE Ratio | Trailing twelve-month earnings ratio |

→ For the math and reasoning behind each metric: [`docs/finance-concepts.md`](docs/finance-concepts.md)

---

## What This Builds Toward

```
📍 Stock Market Dashboard        ← this project
        ↓
Portfolio Optimization           Sharpe Ratio · Efficient Frontier · MPT
        ↓
Factor Investing                 Value · Momentum · Quality factors
        ↓
Algorithmic Trading              Signal generation · Backtesting
        ↓
Risk Management                  Value at Risk · Monte Carlo simulation
```

Every concept implemented here reappears in every project above.

---

## Author

**Rishu Srivastava** · B.Tech CSE · VIT Vellore · 2026  
[Portfolio](https://macos-portfolio-wheat.vercel.app) · [GitHub](https://github.com/rishu-sriv) · [LinkedIn](https://linkedin.com/in/your-handle)