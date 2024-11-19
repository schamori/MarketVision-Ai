from datetime import datetime
from pyalgotrading.algobulls import AlgoBullsConnection
from pyalgotrading.constants import CandleInterval
from torch.backends.opt_einsum import strategy

connection = AlgoBullsConnection()

API_TOKEN = '963eb2015bc36ffddac378301d691bf63ce6c9e8'
connection.set_access_token(API_TOKEN)

from stragety_dqn import StrategySMACrossover

# Upload the strategy
response = connection.create_strategy(StrategySMACrossover, overwrite=True)
all_strategies = connection.get_all_strategies()

strategy_code = all_strategies.iloc[-1]['strategyCode']
print(strategy_code)

strategy_details1 = connection.get_strategy_details(strategy_code)
print(strategy_details1)

# Define strategy parameters
parameters = {
    'TIMEPERIOD1': 10,
    'TIMEPERIOD2': 30
}


# Execute the strategy in live mode
connection.papertrade(
    strategy=strategy_code,          # strategy code
    start='09:15 +0530',             # start time of strategy (HH:MM z)
    end='15:30 +0530',               # end time of strategy (HH:MM z)
    instruments='NSE:SBIN',          # name of the instrument
    lots=1,                          # number of lots per trade
    parameters=parameters,           # parameters required for the strategy
    candle='15 minutes',             # candle size eg : '1 Day', '1 hour', '3 minutes'
)

print(response)