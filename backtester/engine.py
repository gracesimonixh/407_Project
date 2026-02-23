from backtester.portfolio import Portfolio
from backtester.strategies import strategies
import pandas as pd

class BTE:
    def __init__(self, portfolio: Portfolio, strategy: strategies, data: pd.DataFrame):
        self.portfolio = portfolio
        self.strategy = strategy
        self.data = pd.read_csv(data, "data_close_data.csv")
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
            self.strategy(date)
            




    def update_portfolio(self):
        pass

    def get_cur_prices(self):
        pass

    def generate_signals(self):
        pass

    def record_equity(self):
        pass
    


