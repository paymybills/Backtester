"""
Bollinger Bands strategy implementation.
"""

import pandas as pd
import numpy as np
from backtesting_engine.strategies.base_strategy import Strategy

class BollingerBandsStrategy(Strategy):
    """
    Bollinger Bands Strategy.
    Generates buy signals when the price drops below the lower band,
    and sell signals when the price breaks above the upper band.
    """
    
    def __init__(self, period: int = 20, num_std: float = 2.0):
        super().__init__(name=f"BBands_{period}_{num_std}")
        self.period = period
        self.num_std = num_std
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        
        close_col = 'Close' if 'Close' in data.columns else 'close'
        signals['price'] = data[close_col]
        
        # Calculate Bands
        signals['sma'] = data[close_col].rolling(window=self.period).mean()
        signals['std'] = data[close_col].rolling(window=self.period).std()
        signals['upper_band'] = signals['sma'] + (signals['std'] * self.num_std)
        signals['lower_band'] = signals['sma'] - (signals['std'] * self.num_std)
        
        signals['signal'] = 0.0
        
        # Buy when price crosses below lower band
        buy_condition = signals['price'] < signals['lower_band']
        signals.loc[buy_condition, 'signal'] = 1.0
        
        # Sell when price crosses above upper band
        sell_condition = signals['price'] > signals['upper_band']
        signals.loc[sell_condition, 'signal'] = -1.0
        
        signals.loc[signals.index[:self.period], 'signal'] = 0.0
        
        signals['positions'] = signals['signal'].diff().fillna(0.0)
        signals['positions'] = np.sign(signals['positions'])
        
        self.signals = signals
        return signals
