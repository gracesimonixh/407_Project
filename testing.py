# testing.py

import pandas as pd
from backtester.portfolio import Portfolio
from backtester.strategies import TrendFollowing
from backtester.engine import BTE  # assuming your engine class is in engine.py

# -----------------------------
# 1) Setup test data
# -----------------------------
# Tiny dataset: 5 days, 2 tickers
data = pd.DataFrame({
    'Date': ['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05'],
    'AAPL': [100, 101, 102, 103, 104],
    'SPY': [200, 199, 198, 201, 202]
})

# For engine, we need 'date_close_data.csv' format (Date + ticker columns)
data.to_csv('date_close_data.csv', index=False)

# Also save full clean data with all info (here simplified as same data)
data.to_csv('clean_stock_data.csv', index=False)

# -----------------------------
# 2) Initialize Portfolio and Strategy
# -----------------------------
portfolio = Portfolio(start_cash=10000)
strategy = TrendFollowing(short_window=2, long_window=3, position_size=10)

# -----------------------------
# 3) Initialize Backtesting Engine
# -----------------------------
engine = BTE(portfolio=portfolio, strategy=strategy)

# -----------------------------
# 4) Run the backtest
# -----------------------------
engine.run_backtest()

# -----------------------------
# 5) Inspect results
# -----------------------------
print("\nFinal Cash:", portfolio.cash)
print("\nFinal Positions:")
print(portfolio.positions)

print("\nTrades executed:")
for t in portfolio.trades:
    print(t)

print("\nEquity Curve:")
print(portfolio.equity_curve)

# -----------------------------
# 6) Optional: Save equity curve to CSV
# -----------------------------
portfolio.equity_curve.to_csv('equity_curve_test.csv', index=False)
print("\nEquity curve saved to 'equity_curve_test.csv'")