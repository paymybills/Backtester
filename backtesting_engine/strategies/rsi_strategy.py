"""
Relative Strength Index (RSI) strategy implementation.
"""

import pandas as pd
import numpy as np
from backtesting_engine.strategies.base_strategy import Strategy

class RSIStrategy(Strategy):
    """
    RSI Strategy implementation.
    Generates buy signals when RSI falls below the oversold threshold,
    and sell signals when RSI rises above the overbought threshold.
    """
    
    def __init__(self, period: int = 14, oversold: int = 30, overbought: int = 70):
        """
        Initialize the RSI strategy.
        
        Args:
            period: Period for RSI calculation
            oversold: Oversold threshold (usually 30)
            overbought: Overbought threshold (usually 70)
        """
        super().__init__(name=f"RSI_{period}_{oversold}_{overbought}")
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_rsi(self, data: pd.Series) -> pd.Series:
        """
        Calculate the Relative Strength Index.
        
        Args:
            data: Price series (usually close prices)
            
        Returns:
            RSI values as a Series
        """
        delta = data.diff()
        
        # Make two series: one for gains and one for losses
        gains = delta.copy()
        losses = delta.copy()
        
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = abs(losses)
        
        # First average values
        avg_gain = gains[:self.period+1].mean()
        avg_loss = losses[:self.period+1].mean()
        
        # Compute RSI
        rs = avg_gain / avg_loss if avg_loss != 0 else 1.0
        rsi = 100.0 - (100.0 / (1.0 + rs))
        
        # Rest of the data
        for i in range(self.period+1, len(data)):
            avg_gain = (avg_gain * (self.period - 1) + gains.iloc[i]) / self.period
            avg_loss = (avg_loss * (self.period - 1) + losses.iloc[i]) / self.period
            
            rs = avg_gain / avg_loss if avg_loss != 0 else 1.0
            rsi_val = 100.0 - (100.0 / (1.0 + rs))
            
            rsi = pd.concat([rsi, pd.Series([rsi_val], index=[data.index[i]])])
            
        return rsi
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on RSI strategy logic.
        
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
        
        # Calculate RSI
        signals['rsi'] = self.calculate_rsi(data[close_col])
        
        # Create signals
        signals['signal'] = 0
        signals['signal'] = np.where(signals['rsi'] < self.oversold, 1, signals['signal'])  # Buy when oversold
        signals['signal'] = np.where(signals['rsi'] > self.overbought, -1, signals['signal'])  # Sell when overbought
        
        # Generate trading orders: position change
        signals['positions'] = signals['signal'].diff()
        
        # Store the signals for later use
        self.signals = signals
        
        return signals