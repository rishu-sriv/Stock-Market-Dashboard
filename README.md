# Stock Market Dashboard

An interactive financial analysis dashboard built entirely in Python. Fetches live market data from Yahoo Finance, computes return and risk metrics from first principles, and presents everything through a Streamlit web interface — no pre-built financial libraries, no shortcuts.

> Built as a deliberate deep-dive into quantitative finance fundamentals — every metric is implemented manually and understood before it is visualized.

---

## Dashboard Preview

![Stock Dashboard Preview](Screenshot%202026-06-26%20at%2011.33.24%E2%80%AFPM.png)

---

## What This Project Does

Given any publicly listed stock ticker — US or Indian — the dashboard computes and visualizes:

- **Price history** via closing price line chart, OHLC candlestick chart, and volume bars
- **Daily and cumulative returns** calculated from adjusted closing prices using percentage change and compounded growth
- **Return distribution** as a histogram to visualize how returns are spread across trading days
- **Rolling volatility** as annualized standard deviation over a 30-day moving window
- **Company fundamentals** including Market Cap, PE Ratio, EPS, Dividend Yield, Beta, and 52-week range — fetched directly from Yahoo Finance's info endpoint
- **Multi-stock comparison** using normalized prices (base = 100), cumulative return overlays, volatility bars, and a risk vs return scatter map

All metrics update live when the user changes the ticker or time period from the sidebar.

---

## Technical Implementation

### Data Pipeline

```
Yahoo Finance API (via yfinance)
        ↓
fetch_stock_data()       — downloads OHLCV history as a pandas DataFrame
clean_data()             — drops nulls, sorts by date, strips timezone info
fetch_company_info()     — pulls fundamentals from yfinance .info endpoint
        ↓
analysis.py              — all metric computation
visualization.py         — all Plotly figure generation
        ↓
Streamlit (app.py)       — interactive UI layer
```

Data is never hardcoded. Every number on the dashboard is computed live from raw market data.

### Return Calculations

Daily returns are computed as percentage change in adjusted closing price:

```
Daily Return = (Close_t - Close_t-1) / Close_t-1
```

Cumulative returns use compounded multiplication — not summation — because returns compound:

```
Cumulative Return = ∏ (1 + r_t)
```

This distinction matters. A stock that gains 50% then loses 50% does not break even — it ends at 75% of the starting value. Using `.cumprod()` instead of `.cumsum()` captures this correctly.

### Volatility

Annualized volatility is computed as the standard deviation of daily returns scaled by the square root of trading days:

```
Annualized Volatility = σ_daily × √252
```

The √252 scaling comes from the statistical property that variance scales linearly with time — therefore standard deviation scales with the square root. 252 is used because US markets trade approximately 252 days per year.

Rolling volatility uses a 30-day window recalculated daily, producing a time-series of risk rather than a single static number. This reveals when the stock became more or less volatile during the year.

### Normalized Price Comparison

Raw prices cannot be compared across stocks — a $200 stock and a $400 stock tell you nothing about relative performance. Normalization fixes this:

```
Normalized Price = (Price_t / Price_0) × 100
```

Every stock starts at 100 on Day 1. After any period, a value of 118 means 18% growth regardless of the stock's actual price, currency, or share count. This is the standard method used in financial publications for overlaying multiple stocks.

### Risk-Adjusted Return

The comparison table includes a Return/Risk ratio computed as:

```
Return / Risk = Total Return / Annualized Volatility
```

This is a simplified form of the Sharpe Ratio (without the risk-free rate). It answers the question that return alone cannot: *how much return did you earn per unit of risk you accepted?* A stock returning 40% with 50% volatility scores lower than one returning 20% with 15% volatility — and correctly so.

### Caching

All data-fetching functions are wrapped with `@st.cache_data`. The first call fetches from Yahoo Finance and stores the result in memory. Subsequent calls with the same arguments return instantly from cache. This prevents redundant API calls on every user interaction and keeps the dashboard responsive.

---

## Project Structure

```
stock-market-dashboard/
│
├── src/
│   ├── data_loader.py       # Yahoo Finance API calls, company info fetching
│   ├── analysis.py          # Returns, volatility, normalization, comparison logic
│   ├── visualization.py     # All Plotly chart functions
│   └── utils.py             # Data cleaning, formatting, summary printing
│
├── data/                    # Downloaded CSVs (gitignored)
├── assets/                  # Screenshots for README
├── app.py                   # Streamlit dashboard — UI layer only
├── main.py                  # Terminal runner for individual phases
├── requirements.txt
├── .gitignore
└── README.md
```

The codebase is split by responsibility — fetching, analysis, visualization, and UI are each isolated. `app.py` contains no business logic; it only calls functions from `src/`. This makes each module independently testable and reusable in future projects.

---

## Setup

**Requirements:** Python 3.11+

```bash
# Clone
git clone https://github.com/rishu-sriv/stock-market-dashboard.git
cd stock-market-dashboard

# Virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Dependencies
pip install -r requirements.txt

# Launch dashboard
python -m streamlit run app.py
```

> Use `python -m streamlit` to ensure the venv's Streamlit is used, not a system-level installation.

---

## Supported Markets

| Market | Exchange | Suffix | Example |
|---|---|---|---|
| US | NASDAQ / NYSE | _(none)_ | `AAPL`, `MSFT`, `TSLA` |
| India | NSE | `.NS` | `RELIANCE.NS`, `TCS.NS` |
| India | BSE | `.BO` | `INFY.BO`, `HDFCBANK.BO` |
| UK | LSE | `.L` | `HSBA.L`, `BP.L` |
| Germany | XETRA | `.DE` | `SAP.DE`, `BMW.DE` |

Prices are returned in the local currency of the exchange. Normalized comparison removes currency and price-scale differences when comparing across markets.

---

## Finance Concepts Implemented

| Concept | Implementation |
|---|---|
| OHLCV data | Fetched via `yfinance`, cleaned and indexed by date |
| Adjusted Close | Used for all return calculations to account for splits and dividends |
| Daily Return | `pct_change()` on adjusted closing price |
| Cumulative Return | `(1 + r).cumprod()` — compounded, not summed |
| Annualized Volatility | `daily_std × √252` |
| Rolling Volatility | 30-day rolling standard deviation, annualized |
| Normalized Price | `(price / price[0]) × 100` for cross-stock comparison |
| Return/Risk Ratio | Total return divided by annualized volatility |
| Market Cap | Price × shares outstanding, fetched from fundamentals |
| PE Ratio | Trailing twelve months earnings ratio |
| Beta | Sensitivity to market movement, from Yahoo Finance fundamentals |
| 52-Week Range | High/low bounds with current price position |

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.11 |
| Data | yfinance, pandas, numpy |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Environment | venv |
| Version Control | Git |

---

## What This Builds Toward

This project is the foundation of a quantitative finance learning path:

```
Stock Market Dashboard          ← this project
        ↓
Portfolio Optimization          Sharpe Ratio, Efficient Frontier, Modern Portfolio Theory
        ↓
Factor Investing                Value, Momentum, Quality factor construction
        ↓
Algorithmic Trading             Signal generation, backtesting frameworks
        ↓
Risk Management                 Value at Risk (VaR), Monte Carlo simulation
```

Every concept implemented here — returns, volatility, normalization, risk-adjusted metrics — reappears in every project above. The math compounds the same way the returns do.

---

## Author

**Rishu Srivastava**  
B.Tech Computer Science · VIT Vellore · 2026  
[Portfolio](https://macos-portfolio-wheat.vercel.app) · [GitHub](https://github.com/rishu-sriv) · [LinkedIn](https://linkedin.com/in/your-handle)