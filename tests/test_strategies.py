"""
Unit tests for the strategies module.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path so we can import the backtesting engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtesting_engine.strategies import Strategy, MovingAverageCrossover, RSIStrategy

class TestBaseStrategy(unittest.TestCase):
    """Test cases for the base Strategy class."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=100, freq='B')
        data = pd.DataFrame({
            'open': np.random.normal(100, 5, len(dates)),
            'high': np.random.normal(105, 5, len(dates)),
            'low': np.random.normal(95, 5, len(dates)),
            'close': np.random.normal(100, 10, len(dates)),
            'volume': np.random.normal(1000000, 200000, len(dates))
        }, index=dates)
        self.data = data
    
    def test_base_strategy(self):
        """Test the base Strategy class."""
        strategy = Strategy(name="TestStrategy")
        
        # Check initialization
        self.assertEqual(strategy.name, "TestStrategy")
        self.assertIsNone(strategy.signals)
        
        # Check generate_signals (base implementation)
        signals = strategy.generate_signals(self.data)
        
        # Check that signals has same index as data
        self.assertEqual(len(signals), len(self.data))
        self.assertTrue((signals.index == self.data.index).all())
        
        # Check that default signals are all zeros
        self.assertEqual(signals['signal'].sum(), 0)

class TestMAStrategy(unittest.TestCase):
    """Test cases for the MovingAverageCrossover strategy."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample data with a clear trend
        dates = pd.date_range('2020-01-01', periods=300, freq='B')
        
        # Create a price series with a clear trend change
        price = np.zeros(len(dates))
        # First half: uptrend
        price[:150] = np.linspace(100, 150, 150) + np.random.normal(0, 3, 150)
        # Second half: downtrend
        price[150:] = np.linspace(150, 100, 150) + np.random.normal(0, 3, 150)
        
        data = pd.DataFrame({
            'open': price,
            'high': price * 1.01,
            'low': price * 0.99,
            'close': price,
            'volume': np.random.normal(1000000, 200000, len(dates))
        }, index=dates)
        self.data = data
    
    def test_ma_crossover(self):
        """Test the MovingAverageCrossover strategy."""
        # Create MA strategy with short window and long window
        short_window = 10
        long_window = 30
        strategy = MovingAverageCrossover(short_window=short_window, long_window=long_window)
        
        # Check initialization
        self.assertEqual(strategy.name, f"MA_Crossover_{short_window}_{long_window}")
        self.assertEqual(strategy.short_window, short_window)
        self.assertEqual(strategy.long_window, long_window)
        
        # Generate signals
        signals = strategy.generate_signals(self.data)
        
        # Check signal columns
        required_cols = ['price', 'short_ma', 'long_ma', 'signal', 'positions']
        for col in required_cols:
            self.assertIn(col, signals.columns)
        
        # Check that MAs are calculated correctly
        pd.testing.assert_series_equal(
            signals['short_ma'],
            self.data['close'].rolling(window=short_window).mean(),
            check_names=False
        )
        pd.testing.assert_series_equal(
            signals['long_ma'],
            self.data['close'].rolling(window=long_window).mean(),
            check_names=False
        )
        
        # Check that signals are generated only after the long window
        self.assertEqual(signals['signal'].iloc[:long_window].sum(), 0)
        
        # Check that positions contain both buy and sell signals
        positions = signals['positions'].dropna()
        self.assertTrue((positions == 1).any() or (positions == -1).any())

class TestRSIStrategy(unittest.TestCase):
    """Test cases for the RSI strategy."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample data with clear overbought and oversold conditions
        dates = pd.date_range('2020-01-01', periods=200, freq='B')
        price = np.zeros(len(dates))
        
        # Create price pattern that will generate RSI signals
        # Starts with sharp rise (overbought), then sharp fall (oversold), then moderate rise
        for i in range(len(price)):
            if i < 50:
                price[i] = 100 + i * 2  # Sharp rise
            elif i < 100:
                price[i] = 200 - (i - 50) * 2  # Sharp fall
            else:
                price[i] = 100 + (i - 100) * 0.5  # Moderate rise
        
        # Add some noise
        price += np.random.normal(0, 5, len(price))
        
        data = pd.DataFrame({
            'open': price,
            'high': price * 1.01,
            'low': price * 0.99,
            'close': price,
            'volume': np.random.normal(1000000, 200000, len(dates))
        }, index=dates)
        self.data = data
    
    def test_rsi_strategy(self):
        """Test the RSI strategy."""
        # Create RSI strategy with standard parameters
        period = 14
        oversold = 30
        overbought = 70
        strategy = RSIStrategy(period=period, oversold=oversold, overbought=overbought)
        
        # Check initialization
        self.assertEqual(strategy.name, f"RSI_{period}_{oversold}_{overbought}")
        self.assertEqual(strategy.period, period)
        self.assertEqual(strategy.oversold, oversold)
        self.assertEqual(strategy.overbought, overbought)
        
        # Generate signals
        signals = strategy.generate_signals(self.data)
        
        # Check signal columns
        required_cols = ['price', 'rsi', 'signal', 'positions']
        for col in required_cols:
            self.assertIn(col, signals.columns)
        
        # Check that RSI is within bounds
        rsi = signals['rsi'].dropna()
        self.assertTrue((rsi >= 0).all() and (rsi <= 100).all())
        
        # Check that signals are consistent with RSI values
        for i in range(len(signals)):
            if not pd.isna(signals['rsi'].iloc[i]):
                if signals['rsi'].iloc[i] <= oversold:
                    self.assertGreaterEqual(signals['signal'].iloc[i], 0)
                elif signals['rsi'].iloc[i] >= overbought:
                    self.assertLessEqual(signals['signal'].iloc[i], 0)

if __name__ == '__main__':
    unittest.main()