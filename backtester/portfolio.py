import pandas as pd

"""
Variables/notes
    1) start_cash ~ The amount of money you have to trade (before any trades are done)
    2) cash ~ The amount of cash you have
    3) positions ~ How many shares of each stock owned
        ex. Ticker   Shares
             AAPL      10
             SPY        5
    4) portfolio_value ~ Total value of portfolio (position (how many shares) * current price of stock)
    5) equity_curve ~ Record of portfolio value/positions over time
    6) trades ~ A record of every buy or sell action
"""


tickers = ['AAPL', 'JNJ', 'SPY']
class Portfolio:
    def __init__(self, start_cash = 10000):
        self.cash = start_cash
        self.positions = pd.Series(0, index=tickers, dtype=float)
        self.portfolio_value = start_cash
        self.equity_curve = pd.DataFrame(columns=['Cash', 'Portfolio_value'] + tickers)
        self.trades = []
        self.closed_trades = []
        self.open_positions = {}

    def buy(self, ticker, shares, price, date):
        tot_cost = shares*price
        if self.cash < (tot_cost):
            print("Can't make trade, not enough money")
            return
        self.cash -= (tot_cost)
        self.positions[ticker] += shares
        self.trades.append({'date': date, 
                            'action': "BUY", 
                            'ticker': ticker, 
                            'shares': shares, 
                            'price': price, 
                            'notional': tot_cost})
        self.open_positions[ticker] = {"entry_price": price,
                                       "shares": shares, 
                                       "entry_date": date}

    def sell(self, ticker, shares, price, date):
        shares_held = self.positions[ticker]
        if shares_held < shares:
            print("Can't sell, not enough shares")
            return
        
        tot_proceeds = shares*price
        self.cash += tot_proceeds
        self.positions[ticker] -= shares
        self.trades.append({'date': date, 
                            'action': "SELL", 
                            'ticker': ticker, 
                            'shares': shares, 
                            'price': price,
                            'notional': tot_proceeds})

        if self.positions[ticker] == 0 and ticker in self.open_positions:
            entry = self.open_positions.pop(ticker)
            pnl = (price - entry["entry_price"]) * entry["shares"]
            self.closed_trades.append({ "ticker": ticker,
                                        "entry_date": entry["entry_date"],
                                        "exit_date": date,
                                        "entry_price": entry["entry_price"],
                                        "exit_price": price,
                                        "shares": shares,
                                        "pnl": pnl})

    def update(self, current_prices):
        holdings_val = (self.positions * current_prices[tickers]).sum()
        self.portfolio_value = self.cash + holdings_val
    
    def record_equity(self, date):
        #append "snapshot" of cash, positions, portfolio_value to equity curve

        for col in ['Portfolio_value', 'Cash'] + tickers:
            if col not in self.equity_curve.columns:
                self.equity_curve[col] = 0

        new_row = pd.DataFrame({'Cash': [self.cash],
                   'Portfolio_value': [self.portfolio_value]})
        for tick in tickers:
            new_row[tick] = self.positions[tick]

        new_row.index = [date]
        if self.equity_curve.empty:
            self.equity_curve = new_row
        else:
            self.equity_curve = pd.concat([self.equity_curve, new_row])
        