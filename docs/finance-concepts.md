# Finance Concepts — Deep Dive

This document covers the reasoning behind every financial metric implemented in the dashboard. The README links here to keep the main page scannable.

---

## Adjusted Close vs Close

A raw `Close` price can jump overnight because of a stock split or dividend payment — not because the company's value changed. Adjusted Close corrects all historical prices retroactively so the chart looks continuous and comparisons are accurate.

**Rule:** Always use Adjusted Close for return calculations. `yfinance` returns adjusted prices in the `Close` column by default.

---

## Daily Return

```
Daily Return = (Close_t - Close_t-1) / Close_t-1
```

Measures how much the stock gained or lost today relative to yesterday. Expressed as a decimal (0.02 = 2%).

Implemented as `df["Close"].pct_change()`.

---

## Cumulative Return — Why Compounding Matters

```
Cumulative Return = ∏ (1 + r_t)
```

Implemented as `(1 + daily_returns).cumprod()`.

**Why not `.cumsum()`?** Returns compound, they do not add. A stock that gains 50% then loses 50% does not break even:

```
Start:       ₹10,000
After +50%:  ₹15,000
After -50%:  ₹7,500
```

Summation would incorrectly show 0% net return. Multiplication correctly shows -25%.

---

## Annualized Volatility

```
Annualized Volatility = σ_daily × √252
```

Volatility is the standard deviation of daily returns — how much returns vary around their average.

**Why √252?** Variance scales linearly with time. Standard deviation therefore scales with the square root of time. There are approximately 252 trading days in a year (weekends and holidays excluded), so daily volatility is scaled by √252 to produce an annual figure.

| Annualized Volatility | Risk Profile |
|---|---|
| < 15% | Low — utilities, large stable companies |
| 15–25% | Moderate — most large-cap stocks |
| 25–40% | High — growth stocks |
| > 40% | Very High — small-caps, speculative |

---

## Rolling Volatility

A single volatility number for the full year hides when the stock was risky. Rolling volatility recalculates standard deviation over a moving 30-day window every day:

```
Day 30:  σ of Days 1–30
Day 31:  σ of Days 2–31
...
```

This produces a time-series of risk — you can see exactly when volatility spiked (usually around earnings, macro events, or market crises).

---

## Normalized Price

```
Normalized Price = (Price_t / Price_0) × 100
```

You cannot compare a $210 Apple share to a ₹1,500 Reliance share directly. Normalization sets every stock to 100 on Day 1. After any period:

- Value of 118 = 18% growth
- Value of 92 = 8% loss

Currency, share price, and exchange are irrelevant. Only relative growth matters. This is the standard method used in financial publications for overlaying multiple stocks.

---

## Return/Risk Ratio (Simplified Sharpe)

```
Return/Risk = Total Return / Annualized Volatility
```

Return alone is an incomplete metric. A stock returning 40% with 50% volatility is a worse investment than one returning 20% with 12% volatility — the second delivers more return per unit of risk accepted.

The full Sharpe Ratio subtracts the risk-free rate (e.g. treasury yield) from the numerator. This simplified version omits that for clarity, but the logic is identical.

---

## Beta

Beta measures a stock's sensitivity to overall market movement:

| Beta | Meaning |
|---|---|
| 1.0 | Moves exactly with the market |
| 1.5 | Moves 1.5× the market (amplified) |
| 0.5 | Moves half as much (dampened) |
| < 0 | Moves opposite to the market |

If the market drops 10% and a stock has Beta = 1.8, the expected drop is ~18%.

---

## PE Ratio (Price-to-Earnings)

```
PE Ratio = Stock Price / Earnings Per Share
```

Answers: "For every rupee of annual profit this company earns, how much are you paying?"

- PE of 10 → paying ₹10 per ₹1 of profit
- PE of 50 → paying ₹50 per ₹1 of profit

High PE usually means the market expects fast future growth. Low PE may indicate undervaluation — or declining earnings. Always compare PE within the same sector.

---

## Dividend Yield

```
Dividend Yield = Annual Dividends Per Share / Stock Price × 100
```

The percentage of your investment that comes back as cash annually. Mature companies (banks, utilities, FMCG) typically pay dividends. Growth companies reinvest profits instead.

---

*This project is Phase 1 of a quantitative finance learning path. See the README roadmap for what comes next.*