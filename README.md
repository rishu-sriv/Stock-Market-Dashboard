# 📈 Stock Market Dashboard

An interactive stock market analysis dashboard built with Python and Streamlit. Fetches real market data from Yahoo Finance and visualizes price history, returns, volatility, and company fundamentals for any publicly listed stock.

Built as a **learning-first project** — every feature maps to a real finance concept.

---

## Live Demo

> _Add screenshot or GIF of dashboard here once Phase 9 is complete_

---

## Features

- 📊 **Price Charts** — Closing price, candlestick (OHLC), and trading volume
- 📈 **Moving Average** — 20-day simple moving average overlay
- 💹 **Return Analysis** — Daily returns, cumulative returns, best & worst trading days
- 📉 **Volatility Analysis** — Rolling volatility and annualized risk
- 🏢 **Company Fundamentals** — Market Cap, PE Ratio, Dividend Yield, Beta, 52-week range
- 🔄 **Multi-Stock Comparison** — Normalized price comparison across any set of tickers
- 🖥️ **Interactive Dashboard** — Streamlit UI with stock selector, date picker, and CSV download

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.x |
| Data Collection | yfinance |
| Data Analysis | pandas, numpy |
| Visualization | plotly, matplotlib |
| Dashboard | Streamlit |

---

## Project Structure

```
stock-market-dashboard/
│
├── data/                    # Downloaded CSVs (gitignored)
│
├── src/
│   ├── data_loader.py       # Fetch data from Yahoo Finance API
│   ├── analysis.py          # Returns, volatility, metrics
│   ├── visualization.py     # All chart functions
│   └── utils.py             # Helper functions
│
├── app.py                   # Streamlit dashboard
├── main.py                  # Run analysis from terminal
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/stock-market-dashboard.git
cd stock-market-dashboard
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run from terminal**
```bash
python main.py
```

**5. Launch the dashboard**
```bash
streamlit run app.py
```

---

## Usage

### Fetch a single stock
```python
from src.data_loader import fetch_stock_data

df = fetch_stock_data("AAPL", period="1y")
print(df.head())
```

### Fetch an Indian stock
```python
df = fetch_stock_data("RELIANCE.NS", period="1y")   # NSE
df = fetch_stock_data("TCS.BO", period="1y")        # BSE
```

### Fetch multiple stocks
```python
from src.data_loader import fetch_multiple_stocks

stocks = fetch_multiple_stocks(["AAPL", "MSFT", "GOOGL"], period="6mo")
```

### Calculate returns
```python
from src.analysis import calculate_daily_returns, calculate_cumulative_returns

daily = calculate_daily_returns(df)
cumulative = calculate_cumulative_returns(daily)
```

### Compare stocks
```python
from src.visualization import plot_comparison

plot_comparison(["AAPL", "MSFT", "GOOGL"], period="1y")
```

---

## Supported Tickers

Any stock listed on Yahoo Finance works. Examples:

| Market | Examples |
|---|---|
| US (NASDAQ/NYSE) | `AAPL`, `MSFT`, `GOOGL`, `TSLA`, `AMZN` |
| India — NSE | `RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `HDFCBANK.NS` |
| India — BSE | `RELIANCE.BO`, `TCS.BO`, `INFY.BO` |
| UK | `HSBA.L`, `BP.L` |
| Germany | `BMW.DE`, `SAP.DE` |

---

## Finance Concepts Covered

This project is a hands-on introduction to the following concepts:

| Concept | Where It Appears |
|---|---|
| Stock & Ticker Symbol | Phase 2 — data fetching |
| OHLCV Data | Phase 3 — data understanding |
| Closing Price & Adjusted Close | Phase 3 & 4 |
| Moving Average | Phase 4 — price charts |
| Daily Return | Phase 5 — return analysis |
| Cumulative Return | Phase 5 — return analysis |
| Volatility & Standard Deviation | Phase 6 — risk analysis |
| Market Capitalization | Phase 7 — fundamentals |
| PE Ratio | Phase 7 — fundamentals |
| Dividend Yield | Phase 7 — fundamentals |
| Beta | Phase 7 — fundamentals |
| Normalized Price Comparison | Phase 8 — multi-stock |

---

## What I Learned

> _To be filled in as each phase is completed_

- **Phase 2:** How Yahoo Finance API works via yfinance. What ticker symbols are and why Indian stocks use `.NS` / `.BO` suffixes. Why a "1 year" period returns ~252 rows, not 365.
- **Phase 3:** _(coming soon)_
- **Phase 4:** _(coming soon)_

---

## Roadmap

This project is Phase 1 of a larger quantitative finance learning path:

```
📍 Stock Market Dashboard        ← you are here
    ↓
Portfolio Optimization           (Sharpe Ratio, Efficient Frontier)
    ↓
Factor Investing                 (Value, Momentum, Quality)
    ↓
Algorithmic Trading Strategy     (Backtesting, signals)
    ↓
Risk Management                  (VaR, Monte Carlo)
```

---

## Author

**Rishu Srivastava**  
B.Tech CSE 2026 — VIT Vellore  
[Portfolio](https://macos-portfolio-wheat.vercel.app) · [GitHub](https://github.com/rishu-sriv) · [LinkedIn](https://linkedin.com/in/your-handle)

---

## License

MIT License — free to use, modify, and distribute.