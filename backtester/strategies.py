import pandas as pd
from collections import deque

class TrendFollowing:
    def __init__(self, short_window=5, long_window=20, position_size=10):
        """
        Initializes trend following strategy 

        Args: 
            short_window (int): Number of periods for short-term MA 
            long_window (int): Number of periods for long-term MA
            position_size (int): Number of shares per trade
        """

        self.short_window = short_window 
        self.long_window = long_window 
        self.position_size = position_size 

        self.ticker_state = {}

        self.signals = []

    def process_day(self, ticker, close):
        """
        Feeds one day's data to the strategy 

        Args:
            ticker (str): stock ticker symbol
            close (float): closing price for the day
        """

        if ticker not in self.ticker_state:
            self.ticker_state[ticker] = {
                'prices': deque(maxlen=self.long_window),
                'in_position': False 
            }

        state = self.ticker_state[ticker]
        state['prices'].append(close)

        if len(state['prices']) >= self.long_window:
            prices_list = list(state['prices'])

            short_ma = sum(prices_list[-self.short_window:]) / self.short_window 
            long_ma = sum(prices_list) / self.long_window 

            if short_ma > long_ma and not state['in_position']:
                signal = {
                    "ticker": ticker,
                    "action": "BUY", 
                    "quantity": self.position_size
                }
                self.signals.append(signal)
                state['in_position'] = True 

            elif short_ma < long_ma and state['in_position']:
                signal = {
                    "ticker": ticker, 
                    "action": "SELL", 
                    "quantity": self.position_size 
                }
                self.signals.append(signal)
                state['in_position'] = False 

    def get_signals(self): 
        """Return all generated signals"""
        return self.signals

class MeanReversion:
    pass