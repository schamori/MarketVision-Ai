import pandas as pd
import random
from PIL import Image, ImageDraw
import requests
import os
import yfinance as yf
from tqdm import tqdm
import yfinance as yf
from datetime import datetime, timedelta
# API has a limit just for testing
def generate_random_candlestick_data(start_date, num_days):
    dates = pd.date_range(start=start_date, periods=num_days)
    data = {'Date': dates, 'Open': [], 'High': [], 'Low': [], 'Close': []}
    open_price = 100  # Initial price
    for _ in range(num_days):
        daily_open = open_price
        daily_high = daily_open + random.uniform(1, 10)
        daily_low = daily_open - random.uniform(1, 10)
        daily_close = random.uniform(daily_low, daily_high)

        data['Open'].append(daily_open)
        data['High'].append(daily_high)
        data['Low'].append(daily_low)
        data['Close'].append(daily_close)

        open_price = daily_close  # Use the close price of today as the open price of tomorrow

    return pd.DataFrame(data)



def create_candlestick_image(data, width=84, height=84, save_path="candlestick.png"):
    candle_width = 3
    wick_width = 1
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Determine the price range
    price_min = min(data['Low'])
    price_max = max(data['High'])
    price_range = price_max - price_min

    # Normalize price values to pixel positions
    def price_to_pixel(price):
        return height - int((price - price_min) / price_range * (height - 1))

    # Draw each candlestick
    for i, row in enumerate(data.itertuples()):
        pos = i * candle_width

        # Calculate candlestick body
        open_pixel = price_to_pixel(row.Open)
        close_pixel = price_to_pixel(row.Close)
        low_pixel = price_to_pixel(row.Low)
        high_pixel = price_to_pixel(row.High)

        color = 'gray' if row.Close >= row.Open else 'black'

        # Draw the candlestick body
        draw.rectangle([pos, min(open_pixel, close_pixel), pos + candle_width - 1, max(open_pixel, close_pixel)], fill=color)

        # Draw the high-low wicks
        draw.line([pos + candle_width // 2, low_pixel, pos + candle_width // 2, high_pixel], fill=color, width=wick_width)

    image.save(save_path)


def generate_rewards(data, days, csv_file):
    rewards = [data['Close'].iloc[i + days] - data['Close'].iloc[i + days - 1] for i in range(0, len(data) - days - 1)]

    pd.DataFrame(rewards, columns=['Reward']).to_csv(csv_file, index=False)

# df = generate_random_candlestick_data(start_date='2023-04-01', num_days=num_days)
# create_candlestick_image(df, filename='train/0.png')

def data_preparation(stock_symbols, days_per_image = 28, start_date=None, end_date=None, split = 0.71):

    for stock_symbol in tqdm(stock_symbols):
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=days_per_image* 1.5)).strftime('%Y-%m-%d')
        df = yf.Ticker(stock_symbol).history(start=start_date, end=end_date)


        if (len(df) < days_per_image):
            print('No data available for {}'.format(stock_symbol))
            continue
        # Each stock_symbol gets a folder
        os.makedirs(f"train/{stock_symbol}", exist_ok=True)

        os.makedirs(f"test/{stock_symbol}", exist_ok=True)

        df.index = pd.to_datetime(df.index)
        # Save testing plots and rewards
        for i in range(len(df) - days_per_image):
            data_slice = df.iloc[i:i + days_per_image]
            create_candlestick_image(data_slice, save_path=f'test/{stock_symbol}/{i}.png')


if __name__ == '__main__':
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
    data_preparation(stock_symbols)


