from backtester.portfolio import Portfolio
from backtester.strategies import strat1, strat2
import pandas as pd

tickers = ['AAPL', 'JNJ', 'SPY']

class BTE:
    def __init__(self, portfolio: Portfolio, strategy):
        self.portfolio = portfolio
        self.strategy = strategy
        self.data = pd.read_csv ("date_close_data.csv")
        self.alldata = pd.read_csv("clean_stock_data.csv" )
        self.index = self.data.set_index("Date", inplace=True)

    def run_backtest(self):
        """
        Main simulation loop
        Per time step:
            1) gets the current prices
            2) Calls strategy to generate signals
            3) Executes trades based on signals
                if signal = buy (portfolio.buy)
                if signal = sell (portfolio.sell)
            4) Update portfolio value 
            5) Record equity
        Repeats for all time steps 
        """
        for date, row in self.data.iterrows():
            signals = self.strategy.generate_signals(self.alldata, date)
            for signal in signals:
                action = signals[signal]["action"]
                ticker = signals[signal]["ticker"]
                quantity = signals[signal]["quantity"]
                price = row[ticker]

                if action == "BUY":
                    self.portfolio.buy(ticker, quantity, price, date)
                elif action == "SELL":
                    self.portfolio.sell(ticker, quantity, price, date)
            self.portfolio.update(row)
            self.portfolio.record_equity(date)    

    def update_portfolio(self):
        pass

    def get_cur_prices(self):
        pass

    def generate_signals(self):
        pass

    def record_equity(self):
        pass
    


