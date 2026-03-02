"""
Moving Average Convergence Divergence (MACD) strategy implementation.
"""

import pandas as pd
import numpy as np
from backtesting_engine.strategies.base_strategy import Strategy

class MACDStrategy(Strategy):
    """
    MACD Strategy.
    Generates buy signals when MACD line crosses above the Signal line,
    and sell signals when MACD line crosses below the Signal line.
    """
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        super().__init__(name=f"MACD_{fast_period}_{slow_period}_{signal_period}")
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        
        close_col = 'Close' if 'Close' in data.columns else 'close'
        signals['price'] = data[close_col]
        
        # Calculate EMA MACD
        exp_short = data[close_col].ewm(span=self.fast_period, adjust=False).mean()
        exp_long = data[close_col].ewm(span=self.slow_period, adjust=False).mean()
        
        signals['macd'] = exp_short - exp_long
        signals['macd_signal'] = signals['macd'].ewm(span=self.signal_period, adjust=False).mean()
        signals['macd_histogram'] = signals['macd'] - signals['macd_signal']
        
        signals['signal'] = 0.0
        
        # Cross above (buy)
        buy_condition = signals['macd'] > signals['macd_signal']
        signals.loc[buy_condition, 'signal'] = 1.0
        
        # Cross below (sell)
        # Assuming we track crossovers similar to Moving Average logic
        # If it drops below, we map it to 0 and diff later
        # However, purely holding 1 while above and 0 while below handles exits better!
        
        # Hold 0 while below
        sell_condition = signals['macd'] < signals['macd_signal']
        signals.loc[sell_condition, 'signal'] = 0.0
        
        # First `slow_period` points might be unstable due to EMA windup, though EMA handles it gracefully
        # Diff to get positions
        signals['positions'] = signals['signal'].diff().fillna(0.0)
        
        self.signals = signals
        return signals
