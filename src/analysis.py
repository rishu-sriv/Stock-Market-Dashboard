import pandas as pd
import numpy as np


def calculate_daily_returns(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the percentage change in closing price day-over-day.

    Formula: (Today's Close - Yesterday's Close) / Yesterday's Close

    Args:
        df: OHLCV DataFrame with a "Close" column

    Returns:
        Series of daily returns (as decimals, e.g. 0.02 = 2%)
        First row is NaN (no previous day to compare), so it's dropped.
    """
    return df["Close"].pct_change().dropna()


def calculate_cumulative_returns(daily_returns: pd.Series) -> pd.Series:
    """
    Calculate cumulative return from the start date.

    Shows the growth of ₹1 (or $1) invested on Day 1.
    Value of 1.35 means 35% total return.
    Value of 0.85 means 15% total loss.

    Args:
        daily_returns: Series of daily returns from calculate_daily_returns

    Returns:
        Series of cumulative returns starting from ~1.0
    """
    return (1 + daily_returns).cumprod()


def total_return(df: pd.DataFrame) -> float:
    """
    Calculate the total percentage return over the entire period.

    Formula: (Final Price - Initial Price) / Initial Price

    Args:
        df: OHLCV DataFrame

    Returns:
        Total return as a decimal (e.g. 0.167 = 16.7%)
    """
    initial = df["Close"].iloc[0]
    final = df["Close"].iloc[-1]
    return (final - initial) / initial


def best_worst_days(daily_returns: pd.Series, n: int = 5) -> dict:
    """
    Find the best and worst single trading days.

    Args:
        daily_returns: Series of daily returns
        n: Number of days to return (default 5)

    Returns:
        Dict with "best" and "worst" as sorted Series
    """
    return {
        "best": daily_returns.nlargest(n),
        "worst": daily_returns.nsmallest(n)
    }


def return_summary(daily_returns: pd.Series, ticker: str = "") -> None:
    """
    Print a clean summary of return statistics.

    Args:
        daily_returns: Series of daily returns
        ticker: Optional label for display
    """
    label = f" ({ticker})" if ticker else ""
    cumulative = calculate_cumulative_returns(daily_returns)
    total = cumulative.iloc[-1] - 1

    print(f"\n{'='*45}")
    print(f"  Return Summary{label}")
    print(f"{'='*45}")
    print(f"  Total Return         : {total:+.2%}")
    print(f"  Avg Daily Return     : {daily_returns.mean():+.4%}")
    print(f"  Best Single Day      : {daily_returns.max():+.2%}  ({daily_returns.idxmax().date()})")
    print(f"  Worst Single Day     : {daily_returns.min():+.2%}  ({daily_returns.idxmin().date()})")
    print(f"  Positive Days        : {(daily_returns > 0).sum()} / {len(daily_returns)}")
    print(f"  Negative Days        : {(daily_returns < 0).sum()} / {len(daily_returns)}")

def calculate_rolling_volatility(daily_returns: pd.Series, window: int = 30) -> pd.Series:
    """
    Calculate rolling volatility (standard deviation) over a moving window.

    Each value = StdDev of the last `window` days of returns.
    Annualized by multiplying by √252.

    Args:
        daily_returns: Series of daily returns
        window: Rolling window in trading days (default 30)

    Returns:
        Series of annualized rolling volatility values
    """
    return daily_returns.rolling(window=window).std() * (252 ** 0.5)


def annualized_volatility(daily_returns: pd.Series) -> float:
    """
    Calculate a single annualized volatility number for the full period.

    Formula: Daily StdDev × √252

    Args:
        daily_returns: Series of daily returns

    Returns:
        Annualized volatility as a decimal (e.g. 0.22 = 22%)
    """
    return daily_returns.std() * (252 ** 0.5)


def volatility_summary(daily_returns: pd.Series, ticker: str = "") -> None:
    """
    Print a clean volatility and risk summary.

    Args:
        daily_returns: Series of daily returns
        ticker: Optional label for display
    """
    label = f" ({ticker})" if ticker else ""
    vol = annualized_volatility(daily_returns)
    rolling_vol = calculate_rolling_volatility(daily_returns)

    if vol < 0.15:
        risk_label = "Low — stable stock"
    elif vol < 0.25:
        risk_label = "Moderate — typical large-cap"
    elif vol < 0.40:
        risk_label = "High — growth stock territory"
    else:
        risk_label = "Very High — speculative"

    print(f"\n{'='*45}")
    print(f"  Volatility Summary{label}")
    print(f"{'='*45}")
    print(f"  Annualized Volatility : {vol:.2%}")
    print(f"  Risk Profile          : {risk_label}")
    print(f"  Daily StdDev          : {daily_returns.std():.4%}")
    print(f"  Max Rolling Vol       : {rolling_vol.max():.2%}  ({rolling_vol.idxmax().date()})")
    print(f"  Min Rolling Vol       : {rolling_vol.dropna().min():.2%}  ({rolling_vol.dropna().idxmin().date()})")


def compare_volatility(returns_dict: dict) -> None:
    """
    Compare annualized volatility across multiple stocks.

    Args:
        returns_dict: Dict of {ticker: daily_returns_series}
    """
    print(f"\n{'='*45}")
    print(f"  Volatility Comparison")
    print(f"{'='*45}")
    print(f"  {'Ticker':<12} {'Ann. Volatility':<20} {'Risk Profile'}")
    print(f"  {'-'*42}")

    results = {}
    for ticker, returns in returns_dict.items():
        vol = annualized_volatility(returns)
        results[ticker] = vol

    # Sort by volatility, lowest first
    for ticker, vol in sorted(results.items(), key=lambda x: x[1]):
        if vol < 0.15:
            label = "Low"
        elif vol < 0.25:
            label = "Moderate"
        elif vol < 0.40:
            label = "High"
        else:
            label = "Very High"

        print(f"  {ticker:<12} {vol:<20.2%} {label}")