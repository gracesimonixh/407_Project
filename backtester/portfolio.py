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


tickers = ['AAPL', 'SPY']
class Portfolio:
    def __init__(self, start_cash = 10000):
        self.cash = start_cash
        self.positions = pd.Series(0, index=tickers)
        self.portfolio_value = start_cash
        self.equity_curve = pd.DataFrame(columns=['Date', 'Cash', 'Portfolio_Value'] + tickers)
        self.trades = []

    def buy(self, ticker, shares, price, date):
        if self.cash < (shares * price):
            print("Can't make trade, not enough money")
        else:
            self.cash -= (price * shares)
            self.positions[ticker] += shares
            self.trades.append({'date': date, 'action': "BUY", 'ticker': ticker, 'shares': shares, 'price': price})

    def sell(self, ticker, shares, price, date):
        shares_held = self.positions[ticker]
        if shares_held < shares:
            print("Can't sell, not enough shares")
        else:
            self.cash += (shares *  price)
            self.positions[ticker] -= shares
            self.trades.append({'date': date, 'action': "SELL", 'ticker': ticker, 'shares': shares, 'price': price})

    def update(self, current_prices):
        self.portfolio_value = self.cash + (self.positions * current_prices).sum()

    def record_equity(self, date):
        #append "snapshot" of cash, positions, portfolio_value to equity curve
        new_row = {'Date': date, 
                   'Cash': self.cash,
                    'Portfolio_Value': self.portfolio_value}
        for i in range(0, len(tickers)):
            tick = tickers[i]
            new_row.update({tick: self.positions[tick]})
        new_df = pd.DataFrame(new_row)
        self.equity_curve = pd.concat([self.equity_curve, new_row], ignore_index=True)

# 1) Create a portfolio
p = Portfolio(start_cash=10000)

# 2) Simulate some market prices
prices_day1 = pd.Series({'AAPL': 150, 'SPY': 400})

# 3) Buy some stocks
p.buy('AAPL', shares=10, price=150, date='2026-02-01')   # Spend 1500
p.buy('SPY', shares=5, price=400, date='2026-02-01')    # Spend 2000

# 4) Update portfolio value using current prices
p.update(prices_day1)

# 5) Record equity snapshot
p.record_equity(date='2026-02-01')

# 6) Print internal state
print("Cash:", p.cash)
print("\nPositions:")
print(p.positions)

print("\nTrades:")
for t in p.trades:
    print(t)

print("\nEquity Curve:")
print(p.equity_curve)