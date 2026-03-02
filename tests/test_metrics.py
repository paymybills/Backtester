"""
Unit tests for the metrics module.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path so we can import the backtesting engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtesting_engine import Metrics

class TestMetrics(unittest.TestCase):
    """Test cases for the Metrics class."""
    
    def setUp(self):
        """Set up test data."""
        # Create a sample portfolio DataFrame
        dates = pd.date_range('2020-01-01', periods=300, freq='B')
        
        # Create portfolio with an upward trend and some volatility
        trend = np.linspace(0, 30, len(dates))  # Upward trend
        noise = np.random.normal(0, 1, len(dates)) * 0.5
        portfolio_values = 100000 + 1000 * (trend + noise.cumsum())  # Cumulative noise for random walk
        
        # Calculate returns and drawdown
        daily_returns = np.zeros(len(dates))
        daily_returns[1:] = np.diff(portfolio_values) / portfolio_values[:-1]
        cum_returns = (1 + daily_returns).cumprod() - 1
        peak = np.maximum.accumulate(portfolio_values)
        drawdown = (portfolio_values - peak) / peak
        
        # Create DataFrame
        self.portfolio = pd.DataFrame({
            'total': portfolio_values,
            'daily_returns': daily_returns,
            'cum_returns': cum_returns,
            'drawdown': drawdown
        }, index=dates)
        
        # Create benchmark with lower returns
        benchmark_values = 100 + 0.5 * trend + noise.cumsum() * 0.4
        self.benchmark = pd.Series(benchmark_values, index=dates)
    
    def test_calculate_metrics(self):
        """Test that metrics are calculated correctly."""
        metrics = Metrics(self.portfolio, self.benchmark)
        results = metrics.calculate_metrics()
        
        # Check that key metrics are present
        required_metrics = [
            'total_return', 'annualized_return', 'sharpe_ratio', 
            'sortino_ratio', 'max_drawdown', 'calmar_ratio',
            'winning_days', 'avg_win', 'avg_loss', 'win_loss_ratio',
            'beta', 'alpha', 'r_squared'
        ]
        
        for metric in required_metrics:
            self.assertIn(metric, results)
        
        # Check that metrics have reasonable values
        self.assertGreater(results['total_return'], 0)  # Upward trend should have positive return
        self.assertGreater(results['sharpe_ratio'], 0)  # Upward trend should have positive Sharpe
        self.assertLess(results['max_drawdown'], 0)     # Drawdown is negative
        self.assertGreater(results['calmar_ratio'], 0)  # Positive return divided by absolute drawdown
        
        # Check that winning_days is a percentage
        self.assertGreaterEqual(results['winning_days'], 0)
        self.assertLessEqual(results['winning_days'], 1)
    
    def test_drawdown_periods(self):
        """Test identification of drawdown periods."""
        metrics = Metrics(self.portfolio)
        drawdown_periods = metrics.drawdown_periods(threshold=-0.05)
        
        # Check that the function returns a DataFrame
        self.assertIsInstance(drawdown_periods, pd.DataFrame)
        
        # Check for required columns
        required_cols = ['start', 'end', 'duration_days', 'max_drawdown']
        for col in required_cols:
            self.assertIn(col, drawdown_periods.columns)
        
        # Check that max_drawdown values are below the threshold
        if not drawdown_periods.empty:
            self.assertTrue((drawdown_periods['max_drawdown'] <= -0.05).all())
    
    def test_metrics_without_benchmark(self):
        """Test metrics calculation without a benchmark."""
        metrics = Metrics(self.portfolio)  # No benchmark provided
        results = metrics.calculate_metrics()
        
        # Check that key metrics are present
        required_metrics = [
            'total_return', 'annualized_return', 'sharpe_ratio', 
            'sortino_ratio', 'max_drawdown', 'calmar_ratio',
            'winning_days', 'avg_win', 'avg_loss', 'win_loss_ratio',
        ]
        
        for metric in required_metrics:
            self.assertIn(metric, results)
        
        # Check that benchmark-dependent metrics are not present
        benchmark_metrics = ['beta', 'alpha', 'information_ratio']
        for metric in benchmark_metrics:
            self.assertNotIn(metric, results)

if __name__ == '__main__':
    unittest.main()