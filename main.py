from src.data_loader import fetch_stock_data, fetch_company_info
from src.utils import clean_data, print_company_info
from src.visualization import plot_fundamentals_card, plot_52week_range

# Try a few different companies
# Change this ticker and re-run to explore
tickers_to_explore = ["AAPL", "TSLA", "RELIANCE.NS", "HDFCBANK.NS"]

for ticker in tickers_to_explore:
    print(f"\nFetching fundamentals for {ticker}...")
    info = fetch_company_info(ticker)
    print_company_info(info)

# Charts for one stock
ticker = "AAPL"
info = fetch_company_info(ticker)
plot_fundamentals_card(info).show()
plot_52week_range(info).show()