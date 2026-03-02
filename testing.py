# testing.py - FIXED VERSION with CSV EXPORTS
import pandas as pd
from backtester.engine import BTE
from backtester.portfolio import Portfolio
from backtester.strategies import TrendFollowing, MeanReversion
import os

def test_trend_following():
    print("=== TREND FOLLOWING ===")
    
    portfolio = Portfolio(start_cash=10000)
    strategy = TrendFollowing(short_window=5, long_window=20, position_size=10)
    
    engine = BTE(portfolio=portfolio, strategy=strategy)
    performance = engine.run_backtest()
    
    stats = engine.comp_performance(performance)
    
    # EXPORT CSV
    performance.to_csv('trend_following_equity.csv')
    pd.DataFrame(portfolio.closed_trades).to_csv('trend_following_trades.csv', index=False)
    
    print(f"✅ Exported: trend_following_equity.csv ({len(performance)} days)")
    print(f"✅ Exported: trend_following_trades.csv ({len(portfolio.closed_trades)} trades)")
    print(f"Final Value: ${performance['Portfolio_value'].iloc[-1]:,.0f}")
    print(f"Total Return: {((performance['Portfolio_value'].iloc[-1]/10000)-1)*100:.1f}%")
    print()

def test_mean_reversion():
    print("=== MEAN REVERSION ===")
    
    portfolio = Portfolio(start_cash=10000)
    strategy = MeanReversion(mean_window=20, threshold_pct=0.02, position_size=10)
    
    engine = BTE(portfolio=portfolio, strategy=strategy)
    performance = engine.run_backtest()
    
    # EXPORT CSV
    performance.to_csv('mean_reversion_equity.csv')
    pd.DataFrame(portfolio.closed_trades).to_csv('mean_reversion_trades.csv', index=False)
    
    print(f"✅ Exported: mean_reversion_equity.csv ({len(performance)} days)")
    print(f"✅ Exported: mean_reversion_trades.csv ({len(portfolio.closed_trades)} trades)")
    print(f"Final Value: ${performance['Portfolio_value'].iloc[-1]:,.0f}")
    print()

def main():
    print("BACKTESTER TESTS WITH CSV EXPORT")
    data_info = pd.read_csv('Data/date_close_data.csv')
    print(f"Data: {len(data_info)} days ({data_info['Date'].min()} to {data_info['Date'].max()})")
    print("=" * 60)
    
    test_trend_following()
    test_mean_reversion()
    
    print("🎉 All CSVs saved in current folder!")
    print("\nFiles created:")
    for file in os.listdir('.'):
        if file.endswith('.csv') and 'equity' in file or 'trades' in file:
            print(f"  📄 {file}")

if __name__ == "__main__":
    main()
