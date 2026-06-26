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