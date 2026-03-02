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

        
class MeanReversion:
    def __init__(self, mean_window=20, threshold_pct=0.02, position_size=10):
        """"
        Initializes mean reveresion strategy

        Args:
            mean_window (int): number of period for moving average 
            threshold_pct (flaot): percentage distance from mean to trigger entry 
            position_size (int): number of shares per trade
        """

        self.mean_window = mean_window 
        self.threshold_pct = threshold_pct 
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
                'prices': deque(maxlen=self.mean_window),
                'in_position': False,
                'position_type': None
            }
        
        state = self.ticker_state[ticker]
        state['prices'].append(close)

        if len(state['prices']) >= self.mean_window:
            prices_list = list(state['prices'])
            mean = sum(prices_list) / self.mean_window

            upper_band = mean * (1 + self.threshold_pct)
            lower_band = mean * (1 - self.threshold_pct)

            if not state['in_position']:

                if close < lower_band:
                    signal = {
                        "ticker": ticker,
                        "action": "BUY",
                        "quantity": self.position_size
                    }
                    self.signals.append(signal)
                    state['in_position'] = True
                    state['position_type'] = "LONG"

                elif close > upper_band:
                    signal = {
                        "ticker": ticker,
                        "action": "SELL",
                        "quantity": self.position_size
                    }
                    self.signals.append(signal)
                    state['in_position'] = True
                    state['position_type'] = "SHORT"

            else:

                if state['position_type'] == "LONG" and close >= mean:
                    signal = {
                        "ticker": ticker,
                        "action": "SELL",
                        "quantity": self.position_size
                    }
                    self.signals.append(signal)
                    state['in_position'] = False
                    state['position_type'] = None

                elif state['position_type'] == "SHORT" and close <= mean:
                    signal = {
                        "ticker": ticker,
                        "action": "BUY",
                        "quantity": self.position_size
                    }
                    self.signals.append(signal)
                    state['in_position'] = False
                    state['position_type'] = None


