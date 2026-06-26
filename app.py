import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.data_loader import fetch_stock_data, fetch_company_info
from src.utils import clean_data
from src.analysis import (
    calculate_daily_returns,
    calculate_cumulative_returns,
    annualized_volatility,
    total_return,
    best_worst_days,
    normalize_prices,
    build_comparison_data,
)
from src.visualization import (
    plot_closing_price,
    plot_candlestick,
    plot_volume,
    plot_with_moving_average,
    plot_daily_returns,
    plot_return_distribution,
    plot_cumulative_returns,
    plot_rolling_volatility,
    plot_normalized_prices,
    plot_cumulative_returns_comparison,
    plot_return_comparison_bar,
    plot_volatility_comparison_bar,
    plot_risk_return_scatter,
)

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# ── Cached data fetchers ────────────────────────────────────────
@st.cache_data
def load_stock_data(ticker: str, period: str) -> pd.DataFrame:
    df = fetch_stock_data(ticker, period)
    return clean_data(df)

@st.cache_data
def load_company_info(ticker: str) -> dict:
    return fetch_company_info(ticker)

@st.cache_data
def load_comparison_data(tickers_tuple: tuple, period: str) -> dict:
    # Takes a tuple (not list) because lists aren't hashable for caching
    return build_comparison_data(list(tickers_tuple), period)

# ── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.title("📈 Stock Dashboard")
    st.markdown("---")

    mode = st.radio(
        "Mode",
        ["Single Stock", "Compare Stocks"],
        index=0
    )

    st.markdown("---")

    period = st.selectbox(
        "Time Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )

    st.markdown("---")

    if mode == "Single Stock":
        ticker = st.text_input("Ticker Symbol", value="AAPL").upper().strip()
        st.caption("Examples: AAPL, MSFT, TSLA, RELIANCE.NS, TCS.NS")

    else:
        raw = st.text_area(
            "Tickers (one per line)",
            value="AAPL\nMSFT\nGOOGL\nTSLA"
        )
        tickers = [t.strip().upper() for t in raw.strip().split("\n") if t.strip()]

    st.markdown("---")
    st.caption("Data via Yahoo Finance · Built with yfinance + Streamlit")


# ══════════════════════════════════════════════════════════════
# SINGLE STOCK MODE
# ══════════════════════════════════════════════════════════════
if mode == "Single Stock":

    # ── Load data ───────────────────────────────────────────────
    with st.spinner(f"Fetching data for {ticker}..."):
        try:
            df   = load_stock_data(ticker, period)
            info = load_company_info(ticker)
        except Exception as e:
            st.error(f"Could not fetch data for '{ticker}'. Check the ticker symbol.")
            st.stop()

    if df.empty:
        st.error(f"No data returned for '{ticker}'. Try a different ticker or period.")
        st.stop()

    daily_returns      = calculate_daily_returns(df)
    cumulative_returns = calculate_cumulative_returns(daily_returns)
    vol                = annualized_volatility(daily_returns)
    ret                = total_return(df)
    bw                 = best_worst_days(daily_returns, n=1)

    # ── Header ──────────────────────────────────────────────────
    st.title(f"{info.get('name', ticker)}  ({ticker})")
    st.caption(f"{info.get('sector', '')}  ·  {info.get('industry', '')}  ·  {info.get('country', '')}")
    st.markdown("---")

    # ── Top metrics row ─────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)

    current_price = df["Close"].iloc[-1]
    prev_price    = df["Close"].iloc[-2]
    price_delta   = current_price - prev_price

    col1.metric(
        "Current Price",
        f"{current_price:.2f}",
        delta=f"{price_delta:+.2f} today"
    )
    col2.metric("Total Return",       f"{ret:+.2%}")
    col3.metric("Annualized Vol",     f"{vol:.2%}")
    col4.metric("PE Ratio",           f"{info.get('pe_ratio', 'N/A')}")

    market_cap = info.get("market_cap", "N/A")
    if market_cap != "N/A":
        if market_cap >= 1_000_000_000_000:
            market_cap_fmt = f"{market_cap/1_000_000_000_000:.2f}T"
        elif market_cap >= 1_000_000_000:
            market_cap_fmt = f"{market_cap/1_000_000_000:.2f}B"
        else:
            market_cap_fmt = f"{market_cap/1_000_000:.2f}M"
    else:
        market_cap_fmt = "N/A"

    col5.metric("Market Cap",         market_cap_fmt)

    st.markdown("---")

    # ── Price Charts ────────────────────────────────────────────
    st.subheader("📈 Price Charts")

    chart_tab1, chart_tab2, chart_tab3 = st.tabs([
        "Closing Price + MA", "Candlestick", "Volume"
    ])

    with chart_tab1:
        st.plotly_chart(
            plot_with_moving_average(df, ticker, window=20),
            use_container_width=True
        )

    with chart_tab2:
        st.plotly_chart(
            plot_candlestick(df, ticker),
            use_container_width=True
        )

    with chart_tab3:
        st.plotly_chart(
            plot_volume(df, ticker),
            use_container_width=True
        )

    # ── Return Analysis ─────────────────────────────────────────
    st.markdown("---")
    st.subheader("💹 Return Analysis")

    ret_col1, ret_col2 = st.columns(2)

    with ret_col1:
        st.plotly_chart(
            plot_cumulative_returns(cumulative_returns, ticker),
            use_container_width=True
        )

    with ret_col2:
        st.plotly_chart(
            plot_daily_returns(daily_returns, ticker),
            use_container_width=True
        )

    st.plotly_chart(
        plot_return_distribution(daily_returns, ticker),
        use_container_width=True
    )

    # ── Best / Worst Days ───────────────────────────────────────
    st.markdown("---")
    st.subheader("📅 Best & Worst Trading Days")

    bw_full = best_worst_days(daily_returns, n=5)

    bw_col1, bw_col2 = st.columns(2)

    with bw_col1:
        st.markdown("🟢 **Best 5 Days**")
        best_df = (bw_full["best"] * 100).round(2).reset_index()
        best_df.columns = ["Date", "Return (%)"]
        best_df["Date"] = best_df["Date"].dt.date
        st.dataframe(best_df, use_container_width=True, hide_index=True)

    with bw_col2:
        st.markdown("🔴 **Worst 5 Days**")
        worst_df = (bw_full["worst"] * 100).round(2).reset_index()
        worst_df.columns = ["Date", "Return (%)"]
        worst_df["Date"] = worst_df["Date"].dt.date
        st.dataframe(worst_df, use_container_width=True, hide_index=True)

    # ── Volatility ──────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📉 Volatility")

    st.plotly_chart(
        plot_rolling_volatility(daily_returns, ticker, window=30),
        use_container_width=True
    )

    # ── Company Fundamentals ────────────────────────────────────
    st.markdown("---")
    st.subheader("🏢 Company Fundamentals")

    fund_col1, fund_col2 = st.columns(2)

    with fund_col1:
        st.markdown("**Business**")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Country:** {info.get('country', 'N/A')}")
        st.write(f"**Employees:** {info.get('employees', 'N/A'):,}" if isinstance(info.get('employees'), int) else f"**Employees:** N/A")

    with fund_col2:
        st.markdown("**Valuation**")
        st.write(f"**PE Ratio:** {info.get('pe_ratio', 'N/A')}")
        st.write(f"**EPS:** {info.get('eps', 'N/A')}")
        div = info.get('dividend_yield', 'N/A')
        st.write(f"**Dividend Yield:** {div*100:.2f}%" if isinstance(div, float) else f"**Dividend Yield:** N/A")
        st.write(f"**Beta:** {info.get('beta', 'N/A')}")
        st.write(f"**52W High:** {info.get('52w_high', 'N/A')}")
        st.write(f"**52W Low:** {info.get('52w_low', 'N/A')}")

    # ── Download ─────────────────────────────────────────────────
    st.markdown("---")
    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv().encode("utf-8"),
        file_name=f"{ticker}_{period}.csv",
        mime="text/csv"
    )


# ══════════════════════════════════════════════════════════════
# COMPARE STOCKS MODE
# ══════════════════════════════════════════════════════════════
else:

    st.title("📊 Multi-Stock Comparison")
    st.caption(f"Comparing: {', '.join(tickers)}  ·  Period: {period}")
    st.markdown("---")

    if len(tickers) < 2:
        st.warning("Enter at least 2 tickers to compare.")
        st.stop()

    with st.spinner("Fetching data for all tickers..."):
        try:
            comparison_data = load_comparison_data(tuple(tickers), period)
        except Exception as e:
            st.error(f"Error fetching comparison data: {e}")
            st.stop()

    # ── Summary table ────────────────────────────────────────────
    st.subheader("Summary")

    rows = []
    for ticker_key, data in comparison_data.items():
        ret = data["total_return"]
        vol = data["volatility"]
        ratio = ret / vol if vol > 0 else 0
        rows.append({
            "Ticker"        : ticker_key,
            "Total Return"  : f"{ret:+.2%}",
            "Volatility"    : f"{vol:.2%}",
            "Return / Risk" : f"{ratio:.2f}",
        })

    # Sort by total return descending
    rows = sorted(rows, key=lambda x: x["Total Return"], reverse=True)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Normalized price ─────────────────────────────────────────
    st.subheader("📈 Normalized Price (Base = 100)")
    st.caption("Every stock starts at 100 on Day 1. Shows relative growth fairly.")
    st.plotly_chart(
        plot_normalized_prices(comparison_data),
        use_container_width=True
    )

    # ── Cumulative returns ───────────────────────────────────────
    st.subheader("💹 Cumulative Returns")
    st.plotly_chart(
        plot_cumulative_returns_comparison(comparison_data),
        use_container_width=True
    )

    # ── Return and volatility bars ───────────────────────────────
    bar_col1, bar_col2 = st.columns(2)

    with bar_col1:
        st.subheader("Total Return")
        st.plotly_chart(
            plot_return_comparison_bar(comparison_data),
            use_container_width=True
        )

    with bar_col2:
        st.subheader("Volatility")
        st.plotly_chart(
            plot_volatility_comparison_bar(comparison_data),
            use_container_width=True
        )

    # ── Risk / Return scatter ────────────────────────────────────
    st.markdown("---")
    st.subheader("🎯 Risk vs Return Map")
    st.caption("Top-left = ideal (high return, low risk). Bottom-right = worst.")
    st.plotly_chart(
        plot_risk_return_scatter(comparison_data),
        use_container_width=True
    )