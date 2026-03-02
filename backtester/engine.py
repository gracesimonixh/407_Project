import pandas as pd
from backtester.portfolio import Portfolio
from backtester.strategies import TrendFollowing

tickers = ['AAPL', 'JNJ', 'SPY']

"""
Backtesting engine returns:
    1) Equity curve
    2) Trades executed
    3) Final portfolio state
"""

class BTE:
    def __init__(self, portfolio: Portfolio, strategy: TrendFollowing):
        self.portfolio = portfolio
        self.strategy = strategy
        self.data = pd.read_csv("Data/date_close_data.csv")
        self.alldata = pd.read_csv("Data/clean_stock_data.csv")
        self.data.set_index("Date", inplace=True)

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
        if self.portfolio.equity_curve.empty:
            self.portfolio.record_equity(date='START')
        for date, row in self.data.iterrows():
            for ticker in tickers:
                close_price = row[ticker]
                self.strategy.process_day(ticker, close_price)
            signals = self.strategy.signals
            for signal in signals:
                action = signal["action"]
                ticker = signal["ticker"]
                quantity = signal["quantity"]
                price = row[ticker]

                if action == "BUY":
                    self.portfolio.buy(ticker, quantity, price, date)
                elif action == "SELL":
                    self.portfolio.sell(ticker, quantity, price, date)
            self.portfolio.update(row)
            self.portfolio.record_equity(date)  
            self.strategy.signals = []  
        
        performance = self.build_results()
        return performance


    def comp_performance(self, performance):
        """
        Computes performance metrics for analyzing strategy
        - Win rate
        - Total return
        - Maximum Drawdown
        - Average gain/loss
        - Sharpe/Sortino
        - Exposure & Turnover
        """
        equity = performance["Portfolio_value"]
        returns = performance["Daily_Return"].dropna()   
        trades = pd.DataFrame(self.portfolio.closed_trades)

        #sharpe     
        sharpe = returns.mean() / returns.std() * (252 ** 0.5)
        
        #Win rate
        if len(trades) > 0:
            win_rate = (trades["pnl"] > 0).mean()
        #avg gain/loss
            avg_gain = trades[trades["pnl"] > 0]["pnl"].mean()
            avg_loss = trades[trades["pnl"] < 0]["pnl"].mean()
        else:
            win_rate = 0
            avg_gain = 0
            avg_loss = 0

        #total return
        tot_return = equity.iloc[-1] / equity.iloc[0] - 1

        #max drawdown
        max_drawdown = performance["Drawdown"].min()

        #sortino
        downside = returns[returns < 0]
        sortino = returns.mean() / downside.std() * (252 ** 0.5)

        #exposure
        exposure = (performance[tickers].sum(axis=1) > 0).mean()
        
        return {
            "Total Return": tot_return,
            "Sharpe": sharpe,
            "Sortino": sortino,
            "Max Drawdown": max_drawdown,
            "Win Rate": win_rate,
            "Average Gain": avg_gain,
            "Average Loss": avg_loss,
            "Exposure": exposure
        }
    
    def build_results(self):
        print(self.portfolio.equity_curve.head())
        print(self.portfolio.equity_curve.columns)
        equity = self.portfolio.equity_curve.copy()
        if 'Portfolio_value' not in equity.columns:
            raise KeyError()
        equity["Daily_Return"] = equity["Portfolio_value"].pct_change()
        equity["Rolling_Max"] = equity["Portfolio_value"].cummax()
        equity["Drawdown"] = (equity["Portfolio_value"]- equity["Rolling_Max"])/equity["Rolling_Max"]
        return equity