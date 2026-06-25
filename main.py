from src.data_loader import fetch_stock_data, fetch_multiple_stocks, save_to_csv

# --- Test 1: Fetch a single stock ---
print("=== Apple (AAPL) ===")
apple = fetch_stock_data("AAPL", period="1y")

print(f"\nShape: {apple.shape}")          # (rows, columns)
print(f"\nColumns: {apple.columns.tolist()}")
print(f"\nDate range: {apple.index[0]} → {apple.index[-1]}")
print(f"\nFirst 5 rows:")
print(apple.head())

# Save it
save_to_csv(apple, "AAPL_1y")


# --- Test 2: Fetch an Indian stock ---
print("\n=== Reliance Industries (RELIANCE.NS) ===")
reliance = fetch_stock_data("RELIANCE.NS", period="1y")
print(reliance.head())


# --- Test 3: Fetch multiple stocks at once ---
print("\n=== Multiple Stocks ===")
stocks = fetch_multiple_stocks(["AAPL", "MSFT", "GOOGL"], period="6mo")

for ticker, df in stocks.items():
    print(f"{ticker}: {df.shape[0]} trading days of data")