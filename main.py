from src.data_loader import fetch_stock_data
from src.utils import clean_data
from src.visualization import (
    plot_closing_price,
    plot_candlestick,
    plot_volume,
    plot_with_moving_average
)

# Fetch and clean
ticker = "AAPL"
df = fetch_stock_data(ticker, period="1y")
df = clean_data(df)

# Chart 1 — Closing price
fig1 = plot_closing_price(df, ticker)
fig1.show()

# Chart 2 — Candlestick
fig2 = plot_candlestick(df, ticker)
fig2.show()

# Chart 3 — Volume
fig3 = plot_volume(df, ticker)
fig3.show()

# Chart 4 — Price + Moving Average
fig4 = plot_with_moving_average(df, ticker, window=20)
fig4.show()