import yfinance as yf
import pandas as pd

# List of stock symbols
stock_symbols = [
    "KO",
    "PEP",
    "WMT",
    "MCD",
    "T",
    "MSFT",
    "SBUX",
    "INTC",
    "AAPL",
    "V"
]

data = yf.download(stock_symbols, start="2024-10-14", end="2024-10-16", group_by='ticker')

closing_prices = {symbol: data[symbol]['Close'].values[0] for symbol in stock_symbols}

closing_prices_df = pd.DataFrame(list(closing_prices.items()), columns=['Stock Symbol', 'Closing Price (15-10-2024)'])

