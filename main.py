from src.data_loader import fetch_stock_data, fetch_multiple_stocks
from src.utils import clean_data
from src.analysis import (
    calculate_daily_returns,
    volatility_summary,
    compare_volatility
)
from src.visualization import (
    plot_rolling_volatility,
    plot_return_vs_volatility,
    plot_volatility_comparison
)

# --- Single stock volatility ---
ticker = "AAPL"
df = fetch_stock_data(ticker, period="1y")
df = clean_data(df)
daily_returns = calculate_daily_returns(df)

volatility_summary(daily_returns, ticker=ticker)

plot_rolling_volatility(daily_returns, ticker, window=30).show()


# --- Compare multiple stocks ---
tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
stocks = fetch_multiple_stocks(tickers, period="1y")

returns_dict = {}
for t, stock_df in stocks.items():
    stock_df = clean_data(stock_df)
    returns_dict[t] = calculate_daily_returns(stock_df)

# Terminal comparison table
compare_volatility(returns_dict)

# Charts
plot_volatility_comparison(returns_dict).show()
plot_return_vs_volatility(returns_dict).show()