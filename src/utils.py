import pandas as pd


def describe_data(df: pd.DataFrame, ticker: str = "") -> None:
    """
    Print a human-readable summary of the stock DataFrame.

    Args:
        df: OHLCV DataFrame from fetch_stock_data
        ticker: Optional ticker name for display
    """
    label = f" ({ticker})" if ticker else ""

    print(f"{'='*45}")
    print(f"  Stock Data Summary{label}")
    print(f"{'='*45}")

    print(f"\n📅 Date Range")
    print(f"   From : {df.index[0].date()}")
    print(f"   To   : {df.index[-1].date()}")
    print(f"   Days : {len(df)} trading days")

    print(f"\n📋 Columns")
    for col in df.columns:
        print(f"   - {col}")

    print(f"\n💰 Price Range (Close)")
    print(f"   Highest Close : {df['Close'].max():.2f}")
    print(f"   Lowest Close  : {df['Close'].min():.2f}")
    print(f"   Latest Close  : {df['Close'].iloc[-1]:.2f}")

    print(f"\n📊 Volume")
    print(f"   Avg Daily Volume : {df['Volume'].mean():,.0f} shares")
    print(f"   Highest Volume   : {df['Volume'].max():,.0f} shares")

    print(f"\n📈 Sample Data (First 5 rows)")
    print(df[["Open", "High", "Low", "Close", "Volume"]].head())

    print(f"\n🔍 Statistical Summary")
    print(df[["Open", "High", "Low", "Close", "Volume"]].describe().round(2))


def check_missing_values(df: pd.DataFrame) -> None:
    """
    Print missing value count for each column.

    Args:
        df: OHLCV DataFrame
    """
    missing = df.isnull().sum()
    total = len(df)

    print("\n🔎 Missing Values")
    if missing.sum() == 0:
        print("   No missing values found.")
    else:
        for col, count in missing.items():
            if count > 0:
                print(f"   {col}: {count} missing ({count/total:.1%})")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove missing values and ensure data is sorted by date.

    Args:
        df: Raw OHLCV DataFrame

    Returns:
        Cleaned DataFrame
    """
    original_len = len(df)
    df = df.dropna()
    df = df.sort_index()
    removed = original_len - len(df)

    if removed > 0:
        print(f"   Removed {removed} rows with missing values.")
    else:
        print("   Data is clean. No rows removed.")

    return df


def explain_ohlcv() -> None:
    """Print a plain-English explanation of each OHLCV column."""
    explanations = {
        "Open"         : "First trade price when market opened",
        "High"         : "Highest price reached during the day",
        "Low"          : "Lowest price reached during the day",
        "Close"        : "Last trade price before market closed (adjusted)",
        "Volume"       : "Total number of shares traded during the day",
        "Dividends"    : "Cash paid to shareholders on this date (if any)",
        "Stock Splits" : "Share split ratio on this date (if any)",
    }

    print("\n📖 OHLCV Column Guide")
    print(f"{'='*45}")
    for col, meaning in explanations.items():
        print(f"  {col:<15} : {meaning}")