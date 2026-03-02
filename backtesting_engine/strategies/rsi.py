"""
Relative Strength Index (RSI) strategy implementation.
"""

import pandas as pd
import numpy as np
from backtesting_engine.strategies.base_strategy import Strategy

class RSIStrategy(Strategy):
    """
    RSI Strategy.
    Generates buy signals when RSI crosses below the oversold threshold,
    and sell signals when RSI crosses above the overbought threshold.
    """
    
    def __init__(self, period: int = 14, overbought: float = 70.0, oversold: float = 30.0):
        super().__init__(name=f"RSI_{period}_{overbought}_{oversold}")
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        
        close_col = 'Close' if 'Close' in data.columns else 'close'
        signals['price'] = data[close_col]
        
        delta = data[close_col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        rs = gain / loss
        signals['rsi'] = 100 - (100 / (1 + rs))
        
        signals['signal'] = 0.0
        
        # Buy when RSI < oversold
        buy_condition = signals['rsi'] < self.oversold
        signals.loc[buy_condition, 'signal'] = 1.0
        
        # Sell when RSI > overbought
        sell_condition = signals['rsi'] > self.overbought
        signals.loc[sell_condition, 'signal'] = -1.0
        
        signals.loc[signals.index[:self.period], 'signal'] = 0.0
        
        # We hold the position until the signal reverses, so we diff to find actual action points
        signals['positions'] = signals['signal'].diff().fillna(0.0)
        
        # The above logic works for crossover but produces an absolute signal. Standardize:
        # Instead of generic diff which might be 2.0 or -2.0, cap at -1, 0, 1
        signals['positions'] = np.sign(signals['positions'])
        
        self.signals = signals
        return signals
