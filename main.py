from data_preperation import data_preparation

from train import train_dqn
from evaluation import evaluate
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import numpy as np

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

performance = train_dqn(num_episodes=2000)

# Plotting the performance
plt.figure(figsize=(10, 6))
plt.plot( performance, label='Training Performance')
plt.xlabel('Episodes')
plt.ylabel('Cumulative Reward')
plt.title('Training Performance of DQN')
plt.legend()
plt.grid(True)
plt.show()

q_network_path = "weights/weights_best.pth"

# Stock to evalate and visualize
stock_to_evaluate = "MSCI"
total_capital = 4000

evaluate(q_network_path, stock_to_evaluate, total_capital)