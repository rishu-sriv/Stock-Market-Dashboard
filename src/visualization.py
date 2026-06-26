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