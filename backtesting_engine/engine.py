"""
Core backtesting engine implementation for strategy testing and evaluation.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Union

from backtesting_engine.data.data_ingestion import DataIngestion
from backtesting_engine.strategies.base_strategy import Strategy
from backtesting_engine.simulation import Simulation
from backtesting_engine.metrics import Metrics

class BacktestingEngine:
    """
    Main backtesting engine class that coordinates the execution of trading strategies
    and analysis of their performance.
    """
    
    def __init__(self, 
                initial_capital: float = 100000.0,
                commission: float = 0.001,  # 0.1%
                slippage: float = 0.001):    # 0.1%
        """
        Initialize the BacktestingEngine.
        
        Args:
            initial_capital: Starting capital for the backtest
            commission: Trading commission as a fraction of trade value
            slippage: Average slippage as a fraction of trade value
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.data = None
        self.strategies = {}
        self.results = {}
        self.metrics = {}
        self.simulations = {}
    
    def add_data(self, data: pd.DataFrame) -> None:
        """
        Add market data to the backtesting engine.
        
        Args:
            data: DataFrame with market data (OHLCV)
        """
        self.data = data
        # Ensure column names are lowercase for consistency
        self.data.columns = [col.lower() for col in self.data.columns]
        
        # Ensure required columns exist
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in self.data.columns]
        if missing_cols:
            raise ValueError(f"Required columns missing from data: {missing_cols}")
    
    def add_strategy(self, strategy: Strategy) -> None:
        """
        Add a trading strategy to the backtesting engine.
        
        Args:
            strategy: Strategy object to be tested
        """
        self.strategies[strategy.name] = strategy
    
    def run_backtest(self, strategy_name: Optional[str] = None) -> Dict:
        """
        Run the backtest for one or all strategies.
        
        Args:
            strategy_name: Name of the strategy to run, or None to run all strategies
            
        Returns:
            Dictionary with backtest results
        """
        if not self.data is not None:
            raise ValueError("No data provided for backtesting")
        
        # Determine which strategies to run
        if strategy_name:
            if strategy_name not in self.strategies:
                raise ValueError(f"Strategy {strategy_name} not found")
            strategies_to_run = {strategy_name: self.strategies[strategy_name]}
        else:
            strategies_to_run = self.strategies
        
        # Run backtest for each strategy
        for name, strategy in strategies_to_run.items():
            # Generate trading signals
            signals = strategy.generate_signals(self.data)
            
            # Run simulation
            simulation = Simulation(
                data=self.data,
                signals=signals,
                initial_capital=self.initial_capital,
                commission=self.commission,
                slippage=self.slippage
            )
            portfolio = simulation.run()
            self.simulations[name] = simulation
            
            # Calculate performance metrics
            metrics = Metrics(portfolio=portfolio, benchmark=self.data['close'])
            performance = metrics.calculate_metrics()
            
            # Store results
            self.results[name] = {
                'portfolio': portfolio,
                'signals': signals,
                'metrics': performance
            }
            self.metrics[name] = performance
        
        return self.results
    
    def get_results(self, strategy_name: Optional[str] = None) -> Dict:
        """
        Get the results of the backtest.
        
        Args:
            strategy_name: Name of the strategy to get results for, or None for all strategies
            
        Returns:
            Dictionary with backtest results
        """
        if strategy_name:
            if strategy_name not in self.results:
                raise ValueError(f"No results found for strategy {strategy_name}")
            return self.results[strategy_name]
        
        return self.results
    
    def get_metrics(self, strategy_name: Optional[str] = None) -> Dict:
        """
        Get the performance metrics of the backtest.
        
        Args:
            strategy_name: Name of the strategy to get metrics for, or None for all strategies
            
        Returns:
            Dictionary with performance metrics
        """
        if strategy_name:
            if strategy_name not in self.metrics:
                raise ValueError(f"No metrics found for strategy {strategy_name}")
            return self.metrics[strategy_name]
        
        return self.metrics
    
    def compare_strategies(self) -> pd.DataFrame:
        """
        Compare the performance of all strategies.
        
        Returns:
            DataFrame with performance metrics for all strategies
        """
        if not self.metrics:
            raise ValueError("No metrics available. Run backtest first.")
        
        comparison = {}
        for strategy_name, metrics in self.metrics.items():
            comparison[strategy_name] = metrics
        
        return pd.DataFrame(comparison).T