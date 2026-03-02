"""
Basic example of using the backtesting engine to test moving average crossover strategy.
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Add the parent directory to the path so we can import the backtesting engine
sys.path.append(os.path.abspath('..'))

from backtesting_engine import (
    DataIngestion, 
    MovingAverageCrossover,
    BacktestingEngine,
    Reporting
)

def main():
    """Run a simple moving average crossover backtest."""
    print("Starting Moving Average Crossover Backtest")
    
    # Set parameters
    initial_capital = 100000.0
    commission = 0.001  # 0.1%
    
    # Generate sample data
    print("Generating synthetic market data...")
    data_source = DataIngestion()
    data = data_source.generate_sample_data(
        start_date='2020-01-01',
        end_date='2024-01-01',
        ticker='SAMPLE'
    )
    
    # Create the strategy
    print("Creating moving average crossover strategy...")
    ma_strategy = MovingAverageCrossover(short_window=50, long_window=200)
    
    # Initialize the backtesting engine
    print("Initializing backtesting engine...")
    engine = BacktestingEngine(
        initial_capital=initial_capital,
        commission=commission
    )
    
    # Add data and strategy
    engine.add_data(data)
    engine.add_strategy(ma_strategy)
    
    # Run the backtest
    print("Running backtest...")
    results = engine.run_backtest()
    
    # Get performance metrics
    metrics = engine.get_metrics(ma_strategy.name)
    
    # Print performance summary
    reporter = Reporting()
    summary = reporter.generate_performance_summary(metrics)
    print("\n" + summary)
    
    # Create visualization
    print("\nCreating visualizations...")
    portfolio = results[ma_strategy.name]['portfolio']
    
    # Plot equity curve
    fig1 = reporter.plot_equity_curve(portfolio, title=f"{ma_strategy.name} - Equity Curve")
    plt.show()
    
    # Plot drawdown
    fig2 = reporter.plot_drawdown_chart(portfolio, title=f"{ma_strategy.name} - Drawdown")
    plt.show()
    
    # Plot returns distribution
    fig3 = reporter.plot_returns_distribution(portfolio, title=f"{ma_strategy.name} - Returns Distribution")
    plt.show()
    
    print("\nBacktest completed successfully!")

if __name__ == "__main__":
    main()