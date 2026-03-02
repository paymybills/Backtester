"""
Example of comparing multiple strategies using the backtesting engine.
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
    RSIStrategy,
    BacktestingEngine,
    Reporting
)

def main():
    """Run a comparison of moving average crossover and RSI strategies."""
    print("Starting Strategy Comparison Backtest")
    
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
    
    # Create the strategies
    print("Creating strategies...")
    ma_strategy = MovingAverageCrossover(short_window=50, long_window=200)
    rsi_strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    
    # Initialize the backtesting engine
    print("Initializing backtesting engine...")
    engine = BacktestingEngine(
        initial_capital=initial_capital,
        commission=commission
    )
    
    # Add data and strategies
    engine.add_data(data)
    engine.add_strategy(ma_strategy)
    engine.add_strategy(rsi_strategy)
    
    # Run the backtest
    print("Running backtest...")
    results = engine.run_backtest()
    
    # Get comparison metrics
    comparison = engine.compare_strategies()
    print("\nStrategy Comparison:")
    print(comparison[['total_return', 'sharpe_ratio', 'max_drawdown', 'calmar_ratio']])
    
    # Create visualization
    print("\nCreating visualizations...")
    reporter = Reporting()
    
    # Get portfolios for each strategy
    portfolios = {
        strategy_name: result['portfolio']
        for strategy_name, result in results.items()
    }
    
    # Plot strategy comparison
    fig = reporter.plot_strategy_comparison(portfolios, title="Strategy Comparison")
    plt.show()
    
    # Generate HTML report
    print("\nGenerating HTML report...")
    output_path = os.path.join(os.path.dirname(__file__), "strategy_comparison_report.html")
    reporter.save_report_to_html(engine, output_path)
    print(f"Report saved to {output_path}")
    
    print("\nBacktest comparison completed successfully!")

if __name__ == "__main__":
    main()