import plotly.graph_objects as go
import pandas as pd


def plot_closing_price(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Line chart of daily closing prices.

    Args:
        df: OHLCV DataFrame
        ticker: Stock symbol for the chart title

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="#2196F3", width=1.5)
    ))

    fig.update_layout(
        title=f"{ticker} — Closing Price",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig


def plot_candlestick(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Candlestick chart showing Open, High, Low, Close per day.

    Green candle = price closed higher than it opened.
    Red candle   = price closed lower than it opened.

    Args:
        df: OHLCV DataFrame
        ticker: Stock symbol for the chart title

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name=ticker,
        increasing_line_color="#26A69A",   # green
        decreasing_line_color="#EF5350"    # red
    ))

    fig.update_layout(
        title=f"{ticker} — Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,   # cleaner without the slider
        template="plotly_dark"
    )

    return fig


def plot_volume(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Bar chart of daily trading volume.

    Bars are colored green or red to match price direction that day.

    Args:
        df: OHLCV DataFrame
        ticker: Stock symbol for the chart title

    Returns:
        Plotly Figure object
    """
    # Color each bar green if price went up, red if it went down
    colors = [
        "#26A69A" if close >= open_ else "#EF5350"
        for close, open_ in zip(df["Close"], df["Open"])
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volume"],
        name="Volume",
        marker_color=colors
    ))

    fig.update_layout(
        title=f"{ticker} — Trading Volume",
        xaxis_title="Date",
        yaxis_title="Shares Traded",
        template="plotly_dark"
    )

    return fig


def plot_with_moving_average(df: pd.DataFrame, ticker: str, window: int = 20) -> go.Figure:
    """
    Closing price chart with a simple moving average overlay.

    Args:
        df: OHLCV DataFrame
        ticker: Stock symbol for the chart title
        window: Number of days for moving average (default 20)

    Returns:
        Plotly Figure object
    """
    df = df.copy()
    df[f"MA{window}"] = df["Close"].rolling(window=window).mean()

    fig = go.Figure()

    # Closing price
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="#2196F3", width=1.5)
    ))

    # Moving average
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[f"MA{window}"],
        mode="lines",
        name=f"{window}-Day MA",
        line=dict(color="#FF9800", width=2, dash="dot")
    ))

    fig.update_layout(
        title=f"{ticker} — Price with {window}-Day Moving Average",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig

def plot_daily_returns(daily_returns: pd.Series, ticker: str) -> go.Figure:
    """
    Bar chart of daily returns — shows every up and down day.

    Green bars = positive return days
    Red bars   = negative return days

    Args:
        daily_returns: Series of daily returns
        ticker: Stock symbol for the chart title

    Returns:
        Plotly Figure object
    """
    colors = ["#26A69A" if r >= 0 else "#EF5350" for r in daily_returns]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=daily_returns.index,
        y=daily_returns * 100,      # convert to percentage
        name="Daily Return",
        marker_color=colors
    ))

    fig.add_hline(
        y=0,
        line_color="white",
        line_width=0.8,
        opacity=0.4
    )

    fig.update_layout(
        title=f"{ticker} — Daily Returns (%)",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        template="plotly_dark"
    )

    return fig


def plot_return_distribution(daily_returns: pd.Series, ticker: str) -> go.Figure:
    """
    Histogram of daily returns — shows how returns are distributed.

    A tight distribution = stable stock.
    A wide distribution = volatile stock.
    Skew left = more bad days than good.

    Args:
        daily_returns: Series of daily returns
        ticker: Stock symbol for the chart title

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=daily_returns * 100,
        nbinsx=60,
        name="Return Distribution",
        marker_color="#2196F3",
        opacity=0.8
    ))

    # Mark zero with a vertical line
    fig.add_vline(
        x=0,
        line_color="white",
        line_width=1.5,
        opacity=0.6
    )

    # Mark the mean
    mean_return = daily_returns.mean() * 100
    fig.add_vline(
        x=mean_return,
        line_color="#FF9800",
        line_width=2,
        line_dash="dash",
        annotation_text=f"Mean: {mean_return:.2f}%",
        annotation_position="top right"
    )

    fig.update_layout(
        title=f"{ticker} — Daily Return Distribution",
        xaxis_title="Daily Return (%)",
        yaxis_title="Number of Days",
        template="plotly_dark"
    )

    return fig


def plot_cumulative_returns(cumulative_returns: pd.Series, ticker: str) -> go.Figure:
    """
    Line chart showing the growth of ₹1 (or $1) invested from Day 1.

    Value above 1.0 = profit
    Value below 1.0 = loss

    Args:
        cumulative_returns: Series from calculate_cumulative_returns
        ticker: Stock symbol for the chart title

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=cumulative_returns.index,
        y=cumulative_returns,
        mode="lines",
        name="Cumulative Return",
        line=dict(color="#26A69A", width=2),
        fill="tozeroy",
        fillcolor="rgba(38, 166, 154, 0.1)"
    ))

    # Baseline at 1.0 (break-even)
    fig.add_hline(
        y=1.0,
        line_color="white",
        line_width=1,
        line_dash="dot",
        opacity=0.4
    )

    fig.update_layout(
        title=f"{ticker} — Cumulative Return (₹1 invested on Day 1)",
        xaxis_title="Date",
        yaxis_title="Portfolio Value (₹)",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig

def plot_rolling_volatility(daily_returns: pd.Series, ticker: str, window: int = 30) -> go.Figure:
    """
    Line chart of rolling annualized volatility over time.

    Spikes = periods of high uncertainty (crashes, news events)
    Troughs = calm, low-risk periods

    Args:
        daily_returns: Series of daily returns
        ticker: Stock symbol for the chart title
        window: Rolling window in days (default 30)

    Returns:
        Plotly Figure object
    """
    from src.analysis import calculate_rolling_volatility

    rolling_vol = calculate_rolling_volatility(daily_returns, window=window)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=rolling_vol.index,
        y=rolling_vol * 100,           # show as percentage
        mode="lines",
        name=f"{window}-Day Rolling Volatility",
        line=dict(color="#FF9800", width=2),
        fill="tozeroy",
        fillcolor="rgba(255, 152, 0, 0.1)"
    ))

    fig.update_layout(
        title=f"{ticker} — {window}-Day Rolling Volatility (Annualized)",
        xaxis_title="Date",
        yaxis_title="Volatility (%)",
        template="plotly_dark",
        hovermode="x unified"
    )

    return fig


def plot_return_vs_volatility(returns_dict: dict) -> go.Figure:
    """
    Scatter plot comparing return vs volatility across multiple stocks.

    X-axis = annualized volatility (risk)
    Y-axis = total return (reward)

    Stocks in the top-left are ideal: high return, low risk.
    Stocks in the bottom-right are worst: low return, high risk.

    Args:
        returns_dict: Dict of {ticker: daily_returns_series}

    Returns:
        Plotly Figure object
    """
    from src.analysis import annualized_volatility, calculate_cumulative_returns

    tickers, vols, returns = [], [], []

    for ticker, daily_returns in returns_dict.items():
        vol = annualized_volatility(daily_returns)
        total = calculate_cumulative_returns(daily_returns).iloc[-1] - 1
        tickers.append(ticker)
        vols.append(vol * 100)
        returns.append(total * 100)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=vols,
        y=returns,
        mode="markers+text",
        text=tickers,
        textposition="top center",
        marker=dict(size=14, color="#2196F3"),
        name="Stocks"
    ))

    # Reference lines
    fig.add_hline(y=0, line_color="white", line_width=0.8, opacity=0.3)

    fig.update_layout(
        title="Return vs Volatility — Risk/Reward Map",
        xaxis_title="Annualized Volatility / Risk (%)",
        yaxis_title="Total Return (%)",
        template="plotly_dark"
    )

    return fig


def plot_volatility_comparison(returns_dict: dict) -> go.Figure:
    """
    Bar chart comparing annualized volatility across multiple stocks.
    Bars sorted from lowest to highest volatility.

    Args:
        returns_dict: Dict of {ticker: daily_returns_series}

    Returns:
        Plotly Figure object
    """
    from src.analysis import annualized_volatility

    data = {
        ticker: annualized_volatility(returns) * 100
        for ticker, returns in returns_dict.items()
    }

    # Sort lowest to highest
    data = dict(sorted(data.items(), key=lambda x: x[1]))

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(data.keys()),
        y=list(data.values()),
        marker_color="#EF5350",
        name="Annualized Volatility"
    ))

    fig.update_layout(
        title="Annualized Volatility Comparison",
        xaxis_title="Stock",
        yaxis_title="Volatility (%)",
        template="plotly_dark"
    )

    return fig

def plot_fundamentals_card(info: dict) -> go.Figure:
    """
    Visual fundamentals card — displays key metrics as a clean table chart.

    Args:
        info: Dict returned by fetch_company_info

    Returns:
        Plotly Figure object
    """
    def fmt_market_cap(val):
        if val == "N/A":
            return "N/A"
        if val >= 1_000_000_000_000:
            return f"{val / 1_000_000_000_000:.2f}T"
        if val >= 1_000_000_000:
            return f"{val / 1_000_000_000:.2f}B"
        return f"{val / 1_000_000:.2f}M"

    currency = info.get("currency", "")

    metrics = [
        ("Sector",         info["sector"]),
        ("Industry",       info["industry"]),
        ("Market Cap",     f"{fmt_market_cap(info['market_cap'])} {currency}"),
        ("Current Price",  f"{info['current_price']} {currency}"),
        ("PE Ratio",       f"{info['pe_ratio']:.2f}x" if info['pe_ratio'] != "N/A" else "N/A"),
        ("EPS",            f"{info['eps']} {currency}" if info['eps'] != "N/A" else "N/A"),
        ("Dividend Yield", f"{info['dividend_yield']*100:.2f}%" if info['dividend_yield'] != "N/A" else "N/A"),
        ("Beta",           f"{info['beta']:.2f}" if info['beta'] != "N/A" else "N/A"),
        ("52W High",       f"{info['52w_high']} {currency}"),
        ("52W Low",        f"{info['52w_low']} {currency}"),
    ]

    labels = [m[0] for m in metrics]
    values = [m[1] for m in metrics]

    fig = go.Figure(data=[go.Table(
        columnwidth=[200, 300],
        header=dict(
            values=["Metric", "Value"],
            fill_color="#1E1E2E",
            font=dict(color="white", size=13),
            align="left",
            height=35
        ),
        cells=dict(
            values=[labels, values],
            fill_color=[["#2A2A3E", "#252535"] * len(labels)],
            font=dict(color="white", size=12),
            align="left",
            height=30
        )
    )])

    fig.update_layout(
        title=f"{info['name']} ({info['ticker']}) — Company Fundamentals",
        template="plotly_dark",
        margin=dict(t=60, b=20, l=20, r=20)
    )

    return fig


def plot_52week_range(info: dict) -> go.Figure:
    """
    Visual gauge showing where the current price sits
    within the 52-week high/low range.

    Args:
        info: Dict returned by fetch_company_info

    Returns:
        Plotly Figure object
    """
    low = info["52w_low"]
    high = info["52w_high"]
    current = info["current_price"]
    currency = info.get("currency", "")

    if any(v == "N/A" for v in [low, high, current]):
        print("52-week range data not available.")
        return go.Figure()

    # Where is current price as a % of the range
    position_pct = (current - low) / (high - low) * 100

    fig = go.Figure()

    # Range bar background
    fig.add_trace(go.Bar(
        x=["52-Week Range"],
        y=[high - low],
        base=[low],
        marker_color="rgba(255,255,255,0.1)",
        name="52W Range",
        width=0.3
    ))

    # Current price marker
    fig.add_trace(go.Scatter(
        x=["52-Week Range"],
        y=[current],
        mode="markers+text",
        marker=dict(size=16, color="#2196F3", symbol="diamond"),
        text=[f"  {current} {currency}  ({position_pct:.1f}% of range)"],
        textposition="middle right",
        name="Current Price"
    ))

    fig.update_layout(
        title=f"{info['ticker']} — 52-Week Price Range",
        yaxis_title=f"Price ({currency})",
        template="plotly_dark",
        showlegend=True,
        annotations=[
            dict(x=0, y=low, text=f"Low: {low}", showarrow=False,
                 font=dict(color="#EF5350"), xanchor="center", yanchor="top"),
            dict(x=0, y=high, text=f"High: {high}", showarrow=False,
                 font=dict(color="#26A69A"), xanchor="center", yanchor="bottom"),
        ]
    )

    return fig

def plot_normalized_prices(comparison_data: dict) -> go.Figure:
    """
    Overlay normalized price chart for all stocks.

    Every stock starts at 100 on Day 1.
    Shows relative growth fairly regardless of actual price.

    Args:
        comparison_data: Dict returned by build_comparison_data

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    for ticker, data in comparison_data.items():
        fig.add_trace(go.Scatter(
            x=data["normalized"].index,
            y=data["normalized"],
            mode="lines",
            name=ticker,
            line=dict(width=2)
        ))

    # Baseline at 100
    fig.add_hline(
        y=100,
        line_color="white",
        line_width=0.8,
        line_dash="dot",
        opacity=0.4
    )

    fig.update_layout(
        title="Normalized Price Comparison (Base = 100 on Day 1)",
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig


def plot_cumulative_returns_comparison(comparison_data: dict) -> go.Figure:
    """
    Overlay cumulative return chart for all stocks.

    Shows the growth of ₹1 (or $1) invested in each stock on Day 1.

    Args:
        comparison_data: Dict returned by build_comparison_data

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    for ticker, data in comparison_data.items():
        fig.add_trace(go.Scatter(
            x=data["cumulative_returns"].index,
            y=data["cumulative_returns"],
            mode="lines",
            name=ticker,
            line=dict(width=2)
        ))

    fig.add_hline(
        y=1.0,
        line_color="white",
        line_width=0.8,
        line_dash="dot",
        opacity=0.4,
        annotation_text="Break-even",
        annotation_position="left"
    )

    fig.update_layout(
        title="Cumulative Return Comparison",
        xaxis_title="Date",
        yaxis_title="Portfolio Value (₹1 invested)",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig


def plot_return_comparison_bar(comparison_data: dict) -> go.Figure:
    """
    Horizontal bar chart comparing total return across stocks.
    Sorted from highest to lowest return.
    Green = positive return, Red = negative return.

    Args:
        comparison_data: Dict returned by build_comparison_data

    Returns:
        Plotly Figure object
    """
    # Sort by return
    sorted_data = sorted(
        comparison_data.items(),
        key=lambda x: x[1]["total_return"]
    )

    tickers = [d[0] for d in sorted_data]
    returns = [d[1]["total_return"] * 100 for d in sorted_data]
    colors  = ["#26A69A" if r >= 0 else "#EF5350" for r in returns]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=returns,
        y=tickers,
        orientation="h",
        marker_color=colors,
        text=[f"{r:+.2f}%" for r in returns],
        textposition="outside"
    ))

    fig.add_vline(x=0, line_color="white", line_width=1, opacity=0.4)

    fig.update_layout(
        title="Total Return Comparison",
        xaxis_title="Total Return (%)",
        yaxis_title="Stock",
        template="plotly_dark",
        margin=dict(l=100)
    )

    return fig


def plot_risk_return_scatter(comparison_data: dict) -> go.Figure:
    """
    Scatter plot: X = volatility (risk), Y = total return (reward).

    Top-left  = ideal (high return, low risk)
    Bottom-right = worst (low return, high risk)

    Args:
        comparison_data: Dict returned by build_comparison_data

    Returns:
        Plotly Figure object
    """
    tickers = list(comparison_data.keys())
    vols    = [comparison_data[t]["volatility"] * 100 for t in tickers]
    returns = [comparison_data[t]["total_return"] * 100 for t in tickers]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=vols,
        y=returns,
        mode="markers+text",
        text=tickers,
        textposition="top center",
        marker=dict(
            size=14,
            color=returns,
            colorscale="RdYlGn",
            showscale=True,
            colorbar=dict(title="Return %")
        ),
        name="Stocks"
    ))

    fig.add_hline(y=0, line_color="white", line_width=0.8, opacity=0.3)

    fig.update_layout(
        title="Risk vs Return Map  |  Top-left = Best, Bottom-right = Worst",
        xaxis_title="Annualized Volatility / Risk (%)",
        yaxis_title="Total Return (%)",
        template="plotly_dark"
    )

    return fig


def plot_volatility_comparison_bar(comparison_data: dict) -> go.Figure:
    """
    Bar chart comparing annualized volatility across stocks.
    Sorted from lowest to highest risk.

    Args:
        comparison_data: Dict returned by build_comparison_data

    Returns:
        Plotly Figure object
    """
    sorted_data = sorted(
        comparison_data.items(),
        key=lambda x: x[1]["volatility"]
    )

    tickers = [d[0] for d in sorted_data]
    vols    = [d[1]["volatility"] * 100 for d in sorted_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=tickers,
        y=vols,
        marker_color="#FF9800",
        text=[f"{v:.1f}%" for v in vols],
        textposition="outside"
    ))

    fig.update_layout(
        title="Annualized Volatility Comparison (Lower = Less Risky)",
        xaxis_title="Stock",
        yaxis_title="Annualized Volatility (%)",
        template="plotly_dark"
    )

    return fig