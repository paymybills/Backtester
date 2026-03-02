"""Test script to verify signal generation works correctly."""

import sys
import os
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backtesting_engine.data.data_ingestion import DataIngestion
from backtesting_engine.strategies.moving_average import MovingAverageCrossover
from backtesting_engine import BacktestingEngine

print("=" * 60)
print("Testing Signal Generation")
print("=" * 60)

# Test 1: Generate sample data and check column names
print("\n1. Loading Yahoo Finance data for AAPL...")
data_ingestion = DataIngestion()
data = data_ingestion.load_from_yahoo(
    ticker="AAPL",
    start_date="2023-01-01",
    end_date="2023-12-31"
)

if data is None:
    print("ERROR: Failed to load Yahoo Finance data!")
    sys.exit(1)

print(f"   Data shape: {data.shape}")
print(f"   Columns BEFORE engine: {list(data.columns)}")
print(f"   First few rows:")
print(data.head())

# Test 2: Check what happens when we add data to engine
print("\n2. Adding data to BacktestingEngine...")
engine = BacktestingEngine(initial_capital=100000)
engine.add_data(data)

print(f"   Columns AFTER engine: {list(engine.data.columns)}")
print(f"   First few rows:")
print(engine.data.head())

# Test 3: Generate signals with MA strategy
print("\n3. Generating signals with MA Crossover (10/30)...")
strategy = MovingAverageCrossover(short_window=10, long_window=30)
signals = strategy.generate_signals(engine.data)

print(f"   Signals shape: {signals.shape}")
print(f"   Signals columns: {list(signals.columns)}")
print(f"   Signal statistics:")
print(f"     - Total signals: {len(signals)}")
print(f"     - Buy signals (signal=1): {(signals['signal'] == 1).sum()}")
print(f"     - Sell signals (signal=0): {(signals['signal'] == 0).sum()}")
print(f"     - Position changes (!= 0): {(signals['positions'] != 0).sum()}")

# Test 4: Show actual crossover points
print("\n4. Trade signals (where positions change):")
trades = signals[signals['positions'] != 0].copy()
if len(trades) > 0:
    print(f"   Found {len(trades)} potential trades:")
    for idx, row in trades.head(10).iterrows():
        action = "BUY" if row['positions'] > 0 else "SELL"
        print(f"     {idx.date()}: {action} at ${row['price']:.2f}")
else:
    print("   ⚠️  NO TRADES FOUND!")
    print("\n   Debugging info:")
    print(f"   Short MA (10-day) sample: {signals['short_ma'].dropna().head()}")
    print(f"   Long MA (30-day) sample: {signals['long_ma'].dropna().head()}")
    
    # Check if MAs are being calculated
    print(f"\n   Non-null short MA values: {signals['short_ma'].notna().sum()}")
    print(f"   Non-null long MA values: {signals['long_ma'].notna().sum()}")

# Test 5: Run full backtest
print("\n5. Running full backtest...")
engine.add_strategy(strategy)
results = engine.run_backtest(strategy_name=strategy.name)

print(f"   Results keys: {list(results.keys())}")
strategy_name = list(results.keys())[0]
metrics = results[strategy_name]['metrics']

print(f"\n   Performance Metrics:")
print(f"     - Total Return: {metrics.get('total_return', 0)*100:.2f}%")
print(f"     - Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}")
print(f"     - Max Drawdown: {metrics.get('max_drawdown', 0)*100:.2f}%")

portfolio = results[strategy_name]['portfolio']
print(f"\n   Portfolio Summary:")
print(f"     - Starting value: ${portfolio['total'].iloc[0]:.2f}")
print(f"     - Ending value: ${portfolio['total'].iloc[-1]:.2f}")
print(f"     - Peak value: ${portfolio['total'].max():.2f}")

# Check for actual trades in portfolio
position_changes = portfolio['positions'].diff()
actual_trades = portfolio[position_changes != 0]
print(f"\n   Actual trades executed: {len(actual_trades)}")
if len(actual_trades) > 0:
    print(f"   First few trades:")
    print(actual_trades[['price', 'positions', 'cash', 'holdings', 'total']].head())

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
