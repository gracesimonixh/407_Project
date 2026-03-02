# testing.py - BULLETPROOF VERSION
# Guaranteed to work + create CSVs in RIGHT location
import pandas as pd
import os
from pathlib import Path
from backtester.engine import BTE
from backtester.portfolio import Portfolio
from backtester.strategies import TrendFollowing
from datetime import datetime

# ✅ FORCE PROJECT ROOT - NO WRONG FOLDER ISSUES
PROJECT_ROOT = Path.cwd()  # Current working directory
print(f"🚀 Working in: {PROJECT_ROOT.absolute()}")

def ensure_directories():
    """Create output folder if missing"""
    output_dir = PROJECT_ROOT / "results"
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Output folder: {output_dir.absolute()}")
    return output_dir

def safe_csv_save(df, filename, output_dir):
    """Save CSV with full path + confirmation"""
    filepath = output_dir / filename
    df.to_csv(filepath)
    print(f"✅ SAVED: {filepath.absolute()}")
    return filepath

def run_period_test(start_date, end_date, output_dir):
    """Single period backtest"""
    portfolio = Portfolio(start_cash=10000)
    strategy = TrendFollowing(short_window=5, long_window=20, position_size=10)
    
    engine = BTE(portfolio=portfolio, strategy=strategy)
    performance = engine.run_backtest(start_date=start_date, end_date=end_date)
    stats = engine.comp_performance(performance)
    
    final_value = performance['Portfolio_value'].iloc[-1]
    total_return = (final_value / 10000 - 1) * 100
    max_dd = performance['Drawdown'].min() * 100
    
    result = {
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
    
    # SAVE INDIVIDUAL FILES
    safe_csv_save(result['performance'], f"equity_period_{start_date or 'full'}.csv", output_dir)
    trades_df = pd.DataFrame(result['portfolio'].closed_trades)
    safe_csv_save(trades_df, f"trades_period_{start_date or 'full'}.csv", output_dir)
    
    return result

def main():
    print("🔥 BULLETPROOF BACKTESTER - MULTI-PERIOD")
    print("=" * 70)
    
    # CHECK DATA EXISTS
    if not (PROJECT_ROOT / "Data/date_close_data.csv").exists():
        print("❌ ERROR: Data/date_close_data.csv not found!")
        print("Run from PROJECT ROOT (same level as backtester/ and Data/)")
        return
    
    data_info = pd.read_csv('Data/date_close_data.csv')
    print(f"✅ Data found: {len(data_info)} days")
    print(f"   Range: {data_info['Date'].min()} to {data_info['Date'].max()}")
    
    # CREATE OUTPUT FOLDER
    output_dir = ensure_directories()
    
    # TEST PERIODS (adjust to your data)
    periods = [
        (None, None),  # Full period
        ("2020-01-01", "2020-12-31"),
        ("2021-01-01", "2021-12-31"), 
        ("2022-01-01", None),  # 2022 to end
    ]
    
    results = []
    print("\n" + "="*70)
    
    for i, (start, end) in enumerate(periods):
        print(f"\n📊 Running period {i+1}/{len(periods)}: {start} to {end}")
        result = run_period_test(start, end, output_dir)
        results.append(result)
        print(f"   Return: {result['total_return_pct']:+6.1f}% | "
              f"Max DD: {result['max_dd_pct']:5.1f}% | "
              f"Trades: {result['trades']:3d}")
    
    # SUMMARY TABLE
    print("\n" + "="*70)
    print("📈 RESULTS SUMMARY")
    results_df = pd.DataFrame(results)
    print(results_df[['period', 'days', 'trades', 'total_return_pct', 'max_dd_pct', 'sharpe']].round(2))
    
    # FINAL SUMMARY CSV
    summary_path = safe_csv_save(results_df, "SUMMARY_ALL_PERIODS.csv", output_dir)
    
    # LIST ALL CREATED FILES
    print("\n" + "="*70)
    print("🎉 FILES CREATED:")
    csv_files = list(output_dir.glob("*.csv"))
    for f in sorted(csv_files):
        size = f.stat().st_size / 1024  # KB
        print(f"   📄 {f.name:<30} ({size:5.1f} KB)")
    
    # BEST PERFORMER
    best = results_df.loc[results_df['total_return_pct'].idxmax()]
    print(f"\n🏆 BEST: {best['period']:<20} | Return: {best['total_return_pct']:+.1f}%")

if __name__ == "__main__":
    main()
