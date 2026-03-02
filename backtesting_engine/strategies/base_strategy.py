"""
Base strategy module and implementations of common strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict

class Strategy:
    """Base class for implementing trading strategies."""
    
    def __init__(self, name: str = "BaseStrategy"):
        """Initialize the Strategy class."""
        self.name = name
        self.signals = None
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy logic.
        This is a base method to be overridden by specific strategy implementations.
        
        Args:
            data: Market data with OHLCV information
            
        Returns:
            DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Default implementation: no signals
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        self.signals = signals
        return signals