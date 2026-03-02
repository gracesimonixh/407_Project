# testing.py - BOTH STRATEGIES + MULTI-PERIOD (FINAL VERSION)
import pandas as pd
import os
from pathlib import Path
from backtester.engine import BTE
from backtester.portfolio import Portfolio
from backtester.strategies import TrendFollowing, MeanReversion
from datetime import datetime

PROJECT_ROOT = Path.cwd()
print(f"Working in: {PROJECT_ROOT.absolute()}")

def ensure_directories():
    output_dir = PROJECT_ROOT / "results"
    output_dir.mkdir(exist_ok=True)
    print(f"Output folder: {output_dir.absolute()}")
    return output_dir

def safe_csv_save(df, filename, output_dir):
    filepath = output_dir / filename
    df.to_csv(filepath)
    print(f"SAVED: {filepath.absolute()}")
    return filepath

def run_strategy_test(strategy_class, strategy_name, start_date, end_date, output_dir):
    """Test ONE strategy on ONE period"""
    portfolio = Portfolio(start_cash=10000)
    
    if strategy_name == "TrendFollowing":
        strategy = strategy_class(short_window=5, long_window=20, position_size=10)
    else:  # MeanReversion
        strategy = strategy_class(mean_window=20, threshold_pct=0.02, position_size=10)
    
    engine = BTE(portfolio=portfolio, strategy=strategy)
    performance = engine.run_backtest(start_date=start_date, end_date=end_date)
    stats = engine.comp_performance(performance)
    
    final_value = performance['Portfolio_value'].iloc[-1]
    total_return = (final_value / 10000 - 1) * 100
    max_dd = performance['Drawdown'].min() * 100
    
    result = {
        'strategy': strategy_name,
        'period': f"{start_date or 'start'} to {end_date or 'end'}",
        'days': len(performance)-1,
        'trades': len(portfolio.closed_trades),
        'final_value': final_value,
        'total_return_pct': total_return,
        'max_dd_pct': max_dd,
        'sharpe': stats['Sharpe'],
        'performance': performance,
        'portfolio': portfolio
    }
    
    # Save detailed files
    safe_csv_save(result['performance'], 
                 f"{strategy_name}_{start_date or 'full'}_equity.csv", output_dir)
    trades_df = pd.DataFrame(result['portfolio'].closed_trades)
    safe_csv_save(trades_df, 
                 f"{strategy_name}_{start_date or 'full'}_trades.csv", output_dir)
    
    return result

def main():
    print("BOTH STRATEGIES - MULTI-PERIOD BACKTEST")
    print("=" * 70)
    
    if not (PROJECT_ROOT / "Data/date_close_data.csv").exists():
        print("ERROR: Data/date_close_data.csv not found!")
        return
    
    data_info = pd.read_csv('Data/date_close_data.csv')
    print(f"Data: {len(data_info)} days ({data_info['Date'].min()} to {data_info['Date'].max()})")
    
    output_dir = ensure_directories()
    periods = [
        (None, None),           # Full period
        ("2020-01-01", "2020-12-31"),
        ("2021-01-01", "2021-12-31"),
        ("2022-01-01", None),
    ]
    
    all_results = []
    strategies = [
        (TrendFollowing, "TrendFollowing"),
        (MeanReversion, "MeanReversion")
    ]
    
    print("\n" + "="*70)
    print("TESTING BOTH STRATEGIES...")
    
    for strategy_class, strategy_name in strategies:
        print(f"\n{strategy_name}")
        for i, (start, end) in enumerate(periods):
            print(f"  Period {i+1}: {start} to {end}", end=" ... ")
            result = run_strategy_test(strategy_class, strategy_name, start, end, output_dir)
            all_results.append(result)
            print(f"{result['total_return_pct']:+5.1f}% ({result['trades']} trades)")
    

    print("\n" + "="*70)
    print("COMPARISON - BOTH STRATEGIES")
    results_df = pd.DataFrame(all_results)
    
    print(results_df.pivot_table(
        index='period', 
        columns='strategy', 
        values=['total_return_pct', 'trades', 'sharpe'],
        aggfunc='first'
    ).round(2))
    
    # SAVE MASTER SUMMARY
    safe_csv_save(results_df, "BOTH_STRATEGIES_ALL_PERIODS.csv", output_dir)
    
    # BEST OVERALL
    best_overall = results_df.loc[results_df['total_return_pct'].idxmax()]
    print(f"\nBest: {best_overall['strategy']} on {best_overall['period']}")
    print(f"     Return: {best_overall['total_return_pct']:+.1f}% | "
          f"Sharpe: {best_overall['sharpe']:.2f} | "
          f"Drawdown: {best_overall['max_dd_pct']:.1f}%")
    
    # FILE LISTING
    print("\nALL FILES CREATED:")
    csv_files = sorted(output_dir.glob("*.csv"))
    for f in csv_files:
        size = f.stat().st_size / 1024
        print(f"{f.name:<35} ({size:4.1f} KB)")

if __name__ == "__main__":
    main()
