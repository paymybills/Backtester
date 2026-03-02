"""
Moving average crossover strategy implementation.
"""

import pandas as pd
import numpy as np
from backtesting_engine.strategies.base_strategy import Strategy

class MovingAverageCrossover(Strategy):
    """
    Moving Average Crossover strategy.
    Generates buy signals when the short-term MA crosses above the long-term MA,
    and sell signals when the short-term MA crosses below the long-term MA.
    """
    
    def __init__(self, short_window: int = 50, long_window: int = 200):
        """
        Initialize the Moving Average Crossover strategy.
        
        Args:
            short_window: Period of the short-term moving average
            long_window: Period of the long-term moving average
        """
        super().__init__(name=f"MA_Crossover_{short_window}_{long_window}")
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on Moving Average crossover logic.
        
        Args:
            data: Market data with OHLCV information
            
        Returns:
            DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Make a copy of the input data to avoid modifying the original
        signals = pd.DataFrame(index=data.index)
        
        # Handle both uppercase and lowercase column names
        close_col = 'Close' if 'Close' in data.columns else 'close'
        signals['price'] = data[close_col]
        
        # Create short and long moving averages
        signals[f'short_ma'] = data[close_col].rolling(window=self.short_window).mean()
        signals[f'long_ma'] = data[close_col].rolling(window=self.long_window).mean()
        
        # Create signal when short MA crosses above long MA (buy)
        signals['signal'] = 0.0
        
        # Use safe loc assignment to avoid chained indexing
        crossing = signals[f'short_ma'] > signals[f'long_ma']
        signals.loc[crossing, 'signal'] = 1.0
        
        # Ensure the first `long_window` rows don't artificially trigger signals
        signals.loc[signals.index[:self.long_window], 'signal'] = 0.0
        
        # Generate trading orders: -1 for sell, 1 for buy. Fill NA with 0
        signals['positions'] = signals['signal'].diff().fillna(0.0)
        
        # Store the signals for later use
        self.signals = signals
        
        return signals