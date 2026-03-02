"""
Basic unit tests for the backtesting engine.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path so we can import the backtesting engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtesting_engine import (
    DataIngestion,
    Strategy,
    MovingAverageCrossover,
    RSIStrategy,
    BacktestingEngine
)

class TestDataIngestion(unittest.TestCase):
    """Test cases for the DataIngestion class."""
    
    def test_generate_sample_data(self):
        """Test that sample data is generated correctly."""
        data_source = DataIngestion()
        start_date = '2020-01-01'
        end_date = '2020-12-31'
        data = data_source.generate_sample_data(start_date, end_date)
        
        # Check that the data has the correct date range
        self.assertEqual(data.index[0].strftime('%Y-%m-%d'), start_date)
        self.assertTrue(data.index[-1].strftime('%Y-%m-%d') <= end_date)
        
        # Check that the data has the required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            self.assertIn(col, data.columns)
        
        # Check data integrity
        self.assertTrue((data['High'] >= data['Open']).all())
        self.assertTrue((data['High'] >= data['Close']).all())
        self.assertTrue((data['Low'] <= data['Open']).all())
        self.assertTrue((data['Low'] <= data['Close']).all())

class TestStrategy(unittest.TestCase):
    """Test cases for the Strategy classes."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=300, freq='B')
        data = pd.DataFrame({
            'open': np.random.normal(100, 5, len(dates)),
            'high': np.random.normal(105, 5, len(dates)),
            'low': np.random.normal(95, 5, len(dates)),
            'close': np.random.normal(100, 10, len(dates)),
            'volume': np.random.normal(1000000, 200000, len(dates))
        }, index=dates)
        
        # Make sure high is always highest and low is always lowest
        for i in range(len(data)):
            values = [data.iloc[i]['open'], data.iloc[i]['close']]
            data.iloc[i]['high'] = max(values) + abs(np.random.normal(0, 1))
            data.iloc[i]['low'] = min(values) - abs(np.random.normal(0, 1))
        
        self.data = data
    
    def test_ma_crossover_strategy(self):
        """Test that MA Crossover strategy generates signals correctly."""
        strategy = MovingAverageCrossover(short_window=5, long_window=10)
        signals = strategy.generate_signals(self.data)
        
        # Check that the strategy generates signals
        self.assertIn('signal', signals.columns)
        self.assertIn('positions', signals.columns)
        self.assertIn('short_ma', signals.columns)
        self.assertIn('long_ma', signals.columns)
        
        # Check that signals are generated after the long window
        self.assertEqual(signals['signal'].iloc[:10].sum(), 0)
        
        # Check that positions contains both buy and sell signals
        unique_positions = signals['positions'].unique()
        self.assertTrue(any(unique_positions > 0) or any(unique_positions < 0))
    
    def test_rsi_strategy(self):
        """Test that RSI strategy generates signals correctly."""
        strategy = RSIStrategy(period=5, oversold=30, overbought=70)
        signals = strategy.generate_signals(self.data)
        
        # Check that the strategy generates signals
        self.assertIn('signal', signals.columns)
        self.assertIn('positions', signals.columns)
        self.assertIn('rsi', signals.columns)
        
        # Check that RSI values are within range
        self.assertTrue((signals['rsi'].dropna() >= 0).all())
        self.assertTrue((signals['rsi'].dropna() <= 100).all())
        
        # Check that signals are consistent with RSI values
        buy_signals = signals[signals['signal'] == 1]
        sell_signals = signals[signals['signal'] == -1]
        
        if not buy_signals.empty:
            self.assertTrue((buy_signals['rsi'] < strategy.oversold).all())
        if not sell_signals.empty:
            self.assertTrue((sell_signals['rsi'] > strategy.overbought).all())

class TestBacktestingEngine(unittest.TestCase):
    """Test cases for the BacktestingEngine class."""
    
    def setUp(self):
        """Set up test data and strategies."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=300, freq='B')
        trend = np.linspace(0, 30, len(dates))  # Upward trend
        noise = np.random.normal(0, 1, len(dates))
        price = 100 + trend + noise.cumsum()  # Add cumulative noise to create a random walk
        
        data = pd.DataFrame({
            'open': price,
            'high': price * 1.01,
            'low': price * 0.99,
            'close': price,
            'volume': np.random.normal(1000000, 200000, len(dates))
        }, index=dates)
        
        self.data = data
        
        # Create strategies
        self.ma_strategy = MovingAverageCrossover(short_window=50, long_window=200)
        self.rsi_strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    
    def test_engine_initialization(self):
        """Test that the engine initializes correctly."""
        engine = BacktestingEngine(
            initial_capital=100000.0,
            commission=0.001,
            slippage=0.001
        )
        
        self.assertEqual(engine.initial_capital, 100000.0)
        self.assertEqual(engine.commission, 0.001)
        self.assertEqual(engine.slippage, 0.001)
        self.assertEqual(len(engine.strategies), 0)
    
    def test_add_strategy(self):
        """Test adding a strategy to the engine."""
        engine = BacktestingEngine()
        engine.add_strategy(self.ma_strategy)
        engine.add_strategy(self.rsi_strategy)
        
        self.assertEqual(len(engine.strategies), 2)
        self.assertIn(self.ma_strategy.name, engine.strategies)
        self.assertIn(self.rsi_strategy.name, engine.strategies)
    
    def test_run_backtest(self):
        """Test running a backtest."""
        engine = BacktestingEngine()
        engine.add_data(self.data)
        engine.add_strategy(self.ma_strategy)
        
        results = engine.run_backtest()
        
        # Check that results contain the strategy
        self.assertIn(self.ma_strategy.name, results)
        
        # Check that portfolio contains required columns
        portfolio = results[self.ma_strategy.name]['portfolio']
        required_cols = ['total', 'daily_returns', 'cum_returns', 'drawdown']
        for col in required_cols:
            self.assertIn(col, portfolio.columns)
        
        # Check that metrics are calculated
        metrics = engine.get_metrics(self.ma_strategy.name)
        self.assertIsNotNone(metrics)
        self.assertIn('total_return', metrics)
        self.assertIn('sharpe_ratio', metrics)
        self.assertIn('max_drawdown', metrics)
    
    def test_compare_strategies(self):
        """Test comparing multiple strategies."""
        engine = BacktestingEngine()
        engine.add_data(self.data)
        engine.add_strategy(self.ma_strategy)
        engine.add_strategy(self.rsi_strategy)
        
        results = engine.run_backtest()
        comparison = engine.compare_strategies()
        
        # Check that comparison contains both strategies
        self.assertEqual(len(comparison), 2)
        self.assertIn(self.ma_strategy.name, comparison.index)
        self.assertIn(self.rsi_strategy.name, comparison.index)
        
        # Check that comparison contains metrics
        self.assertIn('total_return', comparison.columns)
        self.assertIn('sharpe_ratio', comparison.columns)

if __name__ == '__main__':
    unittest.main()