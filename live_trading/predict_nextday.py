import os
import yfinance as yf

from datetime import datetime, timedelta
from PIL import Image

import dqn.dqn as dqn
from models.StockEnv import StockEnv
import pandas as pd
import torch
from commons import *
from matplotlib.axes import Axes
import numpy as np
import matplotlib.pyplot as plt
from data_preperation import create_candlestick_image


def get_image(image_path):
    """
    Reads the last file in alphabetical order from the folder test/stocksymbol,
    extracts the index from the filename (format: index.png), and loads the image.

    Args:
        stock_symbol (str): The folder name corresponding to the stock symbol.

    Returns:
        img_array (np.ndarray): The image as a NumPy array with shape (1, H, W) or None if no image is found.
        index (int): The extracted index from the filename.
    """

    img = Image.open(image_path).convert('L')  # Convert image to grayscale
    img_array = np.array(img)
    # Add a new dimension at the front (1, H, W)
    return np.expand_dims(img_array, axis=0)


def adjusted_certainty(certainty):
    if certainty <= 70:
        return 0
    elif 70 < certainty < 150:

        return (certainty - 70) / (150 - 70)
    else:
        return 1

def evaluate_dqn(weights_dir, stock, days_per_image=28):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days_per_image * 1.5)).strftime('%Y-%m-%d')

    env = StockEnv(test=True, stock=stock)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    q_network = dqn.QNetworkCNN(action_dim=env.action_space.n).to(device)
    q_network.load_state_dict(torch.load(weights_dir))
    df = yf.Ticker(stock_symbol).history(start=start_date, end=end_date)

    if (len(df) < days_per_image):
        print('No data available for {}'.format(stock_symbol))
        return None, None
    # Get the last 28 stock days
    image_path = f'tmp/{stock_symbol}.png'
    print(len(df[-days_per_image:]))
    create_candlestick_image(df[-days_per_image:], save_path=image_path)

    action, certainty = dqn.evaluate_one_state(q_network, get_image(image_path))


    predicted_growth = (adjusted_certainty(certainty) * 0.05) * action
    return action, predicted_growth


if __name__ == '__main__':
    q_network_path = "../weights_best.pth"
    input_excel = "filled_top_100_tickers.xlsx"
    output_excel = "filled_top_100_tickers.xlsx"

    df = pd.read_excel(input_excel)
    df = df.dropna(subset=["TICKER", "Current Price"])

    if "TICKER" not in df.columns or "Current Price" not in df.columns:
        raise ValueError("The input Excel file must have 'Ticker' and 'Current Price' columns.")

    predicted_prices = []
    predicted_growths = []

    for index, row in df.iterrows():
        stock_symbol = row["TICKER"]
        if not stock_symbol:
            continue
        current_price = row["Current Price"]

        reward, predicted_growth = evaluate_dqn(q_network_path, stock_symbol)
        if reward is None:
            continue
        predicted_price = current_price * (1 + predicted_growth)

        predicted_prices.append(predicted_price)
        predicted_growths.append(predicted_growth * 100)  # Store growth as a percentage

    df["Predicted Growth (%)"] = predicted_growths
    df["Predicted Price by DQN"] = predicted_prices

    df.to_excel(output_excel, index=False)
    print(f"Updated Excel file saved as: {output_excel}")