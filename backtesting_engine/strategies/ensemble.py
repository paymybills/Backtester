"""
Ensemble (Multi-Factor) strategy implementation.
"""

import pandas as pd
import numpy as np
from backtesting_engine.strategies.base_strategy import Strategy

# Import existing strategies to combine them
from backtesting_engine.strategies.moving_average import MovingAverageCrossover
from backtesting_engine.strategies.rsi import RSIStrategy
from backtesting_engine.strategies.macd import MACDStrategy
from backtesting_engine.strategies.bollinger_bands import BollingerBandsStrategy

class EnsembleStrategy(Strategy):
    """
    Combines multiple technical indicators using a voting/weighting mechanism.
    If the combined signal score exceeds a threshold, a trade is executed.
    """
    
    def __init__(self, 
                 weights: dict = None, 
                 buy_threshold: float = 0.6,
                 sell_threshold: float = -0.6):
        
        super().__init__(name="Ensemble_Multi_Factor")
        
        # Default Weights
        if weights is None:
            self.weights = {
                'sma': 0.25,
                'rsi': 0.25,
                'macd': 0.25,
                'bbands': 0.25
            }
        else:
            # Normalize weights just in case
            total = sum(weights.values())
            self.weights = {k: v/total for k, v in weights.items()}
            
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        
        close_col = 'Close' if 'Close' in data.columns else 'close'
        signals['price'] = data[close_col]
        
        # Initialize sub-strategies with standard defaults. 
        # (In a real scenario, these could be passed via constructor)
        sma = MovingAverageCrossover(short_window=50, long_window=200).generate_signals(data)
        rsi = RSIStrategy(period=14, overbought=70, oversold=30).generate_signals(data)
        macd = MACDStrategy(fast_period=12, slow_period=26, signal_period=9).generate_signals(data)
        bbands = BollingerBandsStrategy(period=20, num_std=2).generate_signals(data)
        
        # Extract underlying continuous state intent before diffing
        # E.g., for SMA, signal=1 means long trend, signal=0 means short trend
        # For RSI, signal can be +1 (buy) or -1 (sell)
        
        # Build consensus
        consensus = pd.Series(0.0, index=data.index)
        
        if 'sma' in self.weights:
            sma_mapped = np.where(sma['signal'] == 1, 1, -1)
            consensus += sma_mapped * self.weights['sma']
            
        if 'rsi' in self.weights:
            consensus += rsi['signal'] * self.weights['rsi']
            
        if 'macd' in self.weights:
            macd_mapped = np.where(macd['signal'] == 1, 1, -1)
            consensus += macd_mapped * self.weights['macd']
            
        if 'bbands' in self.weights:
            consensus += bbands['signal'] * self.weights['bbands']
            
        signals['consensus'] = consensus
        
        # Generate absolute holdings signals
        signals['signal'] = 0.0
        
        # If confidence > buy_threshold -> Long
        signals.loc[signals['consensus'] >= self.buy_threshold, 'signal'] = 1.0
        
        # If confidence < sell_threshold -> Close / Short (Engine mostly uses holding 0)
        signals.loc[signals['consensus'] <= self.sell_threshold, 'signal'] = 0.0
        
        # Carry forward previous states for holding periods when confidence is neutral
        signals['signal'] = signals['signal'].replace(0.0, method='ffill').fillna(0.0)
        
        # Compute positions (the diff)
        signals['positions'] = signals['signal'].diff().fillna(0.0)
        
        self.signals = signals
        return signals
