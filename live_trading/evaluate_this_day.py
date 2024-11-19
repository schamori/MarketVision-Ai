import pandas as pd
import yfinance as yf

def simulate_investment(input_excel, output_excel):
    df = pd.read_excel(input_excel)

    if "TICKER" not in df.columns or "Current Price" not in df.columns:
        raise ValueError("The input Excel file must have 'Ticker' and 'Current Price' columns.")

    new_prices = []
    for ticker in df["TICKER"]:
        try:
            stock = yf.Ticker(ticker)
            latest_price = stock.history(period="1d")["Close"].iloc[-1]
            new_prices.append(latest_price)
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            new_prices.append(None)

    percent_gains = []
    money_gains = []

    for index, row in df.iterrows():
        current_price = row["Current Price"]
        new_current_price = new_prices[index]

        if pd.isna(current_price) or pd.isna(new_current_price):
            percent_gains.append(None)
            money_gains.append(None)
            continue

        percent_gain = ((new_current_price - current_price) / current_price) * 100
        money_gain = (percent_gain / 100) * 1000

        percent_gains.append(percent_gain)
        money_gains.append(money_gain)

    df["New Current Price"] = new_prices
    df["Percent Gain (%)"] = percent_gains
    df["Money Gain ($)"] = money_gains

    avg_percent_gain = df["Percent Gain (%)"].mean()
    avg_money_gain = df["Money Gain ($)"].mean()

    averages = {
        "Ticker": "Average",
        "Current Price": None,
        "New Current Price": None,
        "Percent Gain (%)": avg_percent_gain,
        "Money Gain ($)": avg_money_gain,
    }
    df = df.append(averages, ignore_index=True)

    df.to_excel(output_excel, index=False)
    print(f"Updated Excel file saved as: {output_excel}")

input_excel = "../filled_top_100_tickers.xlsx"
output_excel = "stocks_with_investment_simulation.xlsx"
simulate_investment(input_excel, output_excel)
