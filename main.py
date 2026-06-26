from src.data_loader import fetch_stock_data
from src.utils import describe_data, check_missing_values, clean_data, explain_ohlcv

# Fetch data
apple = fetch_stock_data("AAPL", period="1y")

# Understand the columns
explain_ohlcv()

# Full summary
describe_data(apple, ticker="AAPL")

# Check data quality
check_missing_values(apple)

# Clean it
apple = clean_data(apple)

# One specific thing to notice:
# High is always >= Open, Close, Low
# Low is always <= Open, Close, High
# Verify this yourself:
print("\n✅ Sanity Checks")
print(f"High >= Close always: {(apple['High'] >= apple['Close']).all()}")
print(f"Low  <= Close always: {(apple['Low']  <= apple['Close']).all()}")
print(f"High >= Low   always: {(apple['High'] >= apple['Low']).all()}")