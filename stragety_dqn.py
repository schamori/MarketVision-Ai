from pyalgotrading.strategy.strategy_base import StrategyBase
from pyalgotrading.constants import *

class StrategySMACrossover(StrategyBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeperiod1 = self.strategy_parameters['TIMEPERIOD1']
        self.timeperiod2 = self.strategy_parameters['TIMEPERIOD2']

    def initialize(self):
        self.main_order = {}

    @staticmethod
    def name():
        return 'SMA Crossover Strategy'



    def strategy_select_instruments_for_entry(self, candle, instruments_bucket, instruments_in_portfolio):
        crossover_value = self.get_crossover_value(candle)
        if crossover_value > 0:
            return [candle.symbol]
        return []

    def strategy_enter_position(self, candle, instrument):
        self.main_order[instrument] = self.broker.buy_order_regular(instrument=instrument, quantity=1)

    def strategy_select_instruments_for_exit(self, candle, instruments_in_portfolio):
        crossover_value = self.get_crossover_value(candle)
        if crossover_value < 0:
            return [candle.symbol]
        return []

    def strategy_exit_position(self, candle, instrument):
        self.broker.exit_position(instrument)

    def get_crossover_value(self, candle):
        sma1 = self.broker.get_sma(candle.symbol, self.timeperiod1)
        sma2 = self.broker.get_sma(candle.symbol, self.timeperiod2)
        return sma1 - sma2