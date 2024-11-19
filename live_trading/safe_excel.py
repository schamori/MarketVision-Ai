import pandas as pd
import yfinance as yf
from data_preperation import create_candlestick_image


def fetch_stock_prices(input_file, output_file):
    # Read the Excel file
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Check if 'Ticker' column exists
    if 'TICKER' not in df.columns:
        print("The Excel file must have a 'Ticker' column.")
        return

    # Initialize a list to store current prices
    current_prices = []

    # Fetch the closing prices for each ticker
    for ticker in df['TICKER']:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1d')
            if not hist.empty:
                current_prices.append(hist['Close'].iloc[-1])
            else:
                current_prices.append(None)  # Append None if no data is found
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            current_prices.append(None)

    # Add the 'Current Price' column to the DataFrame
    df['Current Price'] = current_prices

    # Save the updated DataFrame to a new Excel file
    try:
        df.to_excel(output_file, index=False)
        print(f"Updated Excel file saved as: {output_file}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")
# Example usage
input_file = '../top_100_tickers.xlsx'
output_file = '../filled_top_100_tickers.xlsx'
fetch_stock_prices(input_file, output_file)
