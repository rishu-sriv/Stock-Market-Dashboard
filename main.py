from src.analysis import build_comparison_data, print_comparison_table
from src.visualization import (
    plot_normalized_prices,
    plot_cumulative_returns_comparison,
    plot_return_comparison_bar,
    plot_risk_return_scatter,
    plot_volatility_comparison_bar
)

# --- US Tech Giants ---
print("\n📊 US Tech Comparison")
us_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
us_data = build_comparison_data(us_tickers, period="1y")

print_comparison_table(us_data)

plot_normalized_prices(us_data).show()
plot_cumulative_returns_comparison(us_data).show()
plot_return_comparison_bar(us_data).show()
plot_volatility_comparison_bar(us_data).show()
plot_risk_return_scatter(us_data).show()


# --- Indian Blue Chips ---
print("\n📊 Indian Market Comparison")
in_tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
in_data = build_comparison_data(in_tickers, period="1y")

print_comparison_table(in_data)

plot_normalized_prices(in_data).show()
plot_risk_return_scatter(in_data).show()