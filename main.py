from src.data_loader import fetch_stock_data
from src.utils import clean_data
from src.analysis import (
    calculate_daily_returns,
    calculate_cumulative_returns,
    total_return,
    best_worst_days,
    return_summary
)
from src.visualization import (
    plot_daily_returns,
    plot_return_distribution,
    plot_cumulative_returns
)

# Fetch and clean
ticker = "AAPL"
df = fetch_stock_data(ticker, period="1y")
df = clean_data(df)

# Calculate returns
daily_returns = calculate_daily_returns(df)
cumulative_returns = calculate_cumulative_returns(daily_returns)

# Print summary
return_summary(daily_returns, ticker=ticker)

# Best and worst days
bw = best_worst_days(daily_returns, n=5)
print("\n🟢 Best 5 Trading Days")
print((bw["best"] * 100).round(2).to_string())
print("\n🔴 Worst 5 Trading Days")
print((bw["worst"] * 100).round(2).to_string())

# Charts
plot_daily_returns(daily_returns, ticker).show()
plot_return_distribution(daily_returns, ticker).show()
plot_cumulative_returns(cumulative_returns, ticker).show()