"""
Simulation module to execute trading strategies on historical data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class Simulation:
    """
    Simulation class that executes trading strategies on historical data
    and tracks portfolio performance.
    """
    
    def __init__(self, 
                data: pd.DataFrame,
                signals: pd.DataFrame,
                initial_capital: float = 100000.0,
                commission: float = 0.001,  # 0.1%
                slippage: float = 0.001):   # 0.1%
        """
        Initialize the Simulation class.
        
        Args:
            data: Market data with OHLCV information
            signals: Trading signals (1 for buy, -1 for sell, 0 for hold)
            initial_capital: Starting capital for the simulation
            commission: Trading commission as a fraction of trade value
            slippage: Average slippage as a fraction of trade value
        """
        self.data = data
        self.signals = signals
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.portfolio = None
    
    def run(self) -> pd.DataFrame:
        """
        Run the simulation and track portfolio performance.
        
        Returns:
            DataFrame with portfolio values and performance metrics
        """
        # Ensure required columns exist
        if 'positions' not in self.signals.columns:
            raise ValueError("Signal DataFrame must contain 'positions' column")
        if 'price' not in self.signals.columns:
            self.signals['price'] = self.data['close']
        
        # Initialize portfolio DataFrame
        portfolio = pd.DataFrame(index=self.signals.index)
        portfolio['price'] = self.signals['price']
        portfolio['signal'] = self.signals['signal']
        portfolio['positions'] = self.signals['positions']
        
        # Position sizing - assume fully invested
        portfolio['holdings'] = 0.0
        portfolio['cash'] = self.initial_capital
        portfolio['total'] = self.initial_capital
        
        # Track number of shares held
        shares_held = 0
        
        # Simulate trading
        for i, date in enumerate(portfolio.index):
            # If this is the first data point, skip (no previous data to act on)
            if i == 0:
                continue
                
            # Get current signal
            current_signal = portfolio.loc[date, 'positions']
            current_price = portfolio.loc[date, 'price']
            
            # Calculate transaction costs (commission + slippage)
            transaction_cost_rate = self.commission + self.slippage
            
            # Update holdings based on signals
            if current_signal != 0:  # If there's a trade
                # For buy signals
                if current_signal > 0:
                    # Determine how much to invest
                    available_cash = portfolio.loc[portfolio.index[i-1], 'cash']
                    investment_amount = available_cash * 0.95  # Keep some cash reserve
                    
                    # Calculate shares to buy (accounting for transaction costs)
                    shares_to_buy = int(investment_amount / (current_price * (1 + transaction_cost_rate)))
                    
                    # Update holdings
                    if shares_to_buy > 0:
                        shares_held += shares_to_buy
                        cost = shares_to_buy * current_price * (1 + transaction_cost_rate)
                        portfolio.loc[date, 'cash'] = available_cash - cost
                    else:
                        # Fallback if we can't afford shares
                        portfolio.loc[date, 'cash'] = portfolio.loc[portfolio.index[i-1], 'cash']
                
                # For sell signals
                elif current_signal < 0 and shares_held > 0:
                    # Sell all shares
                    sell_value = shares_held * current_price * (1 - transaction_cost_rate)
                    portfolio.loc[date, 'cash'] = portfolio.loc[portfolio.index[i-1], 'cash'] + sell_value
                    shares_held = 0
                else:
                    # Fallback if signal was sell but we have no shares
                    portfolio.loc[date, 'cash'] = portfolio.loc[portfolio.index[i-1], 'cash']
            
            # If no trade, cash remains the same
            else:
                portfolio.loc[date, 'cash'] = portfolio.loc[portfolio.index[i-1], 'cash']
            
            # Update holdings value and total portfolio value
            portfolio.loc[date, 'holdings'] = shares_held * current_price
            portfolio.loc[date, 'total'] = portfolio.loc[date, 'cash'] + portfolio.loc[date, 'holdings']
        
        # Calculate daily returns
        portfolio['daily_returns'] = portfolio['total'].pct_change()
        
        # Calculate cumulative returns
        portfolio['cum_returns'] = (1 + portfolio['daily_returns']).cumprod() - 1
        
        # Calculate drawdown
        portfolio['peak'] = portfolio['total'].cummax()
        portfolio['drawdown'] = (portfolio['total'] - portfolio['peak']) / portfolio['peak']
        
        self.portfolio = portfolio
        return portfolio