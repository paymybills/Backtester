"""
Parameter Sweep Optimizer for testing hundreds of strategy combinations.
"""

import pandas as pd
import numpy as np
import itertools
from typing import Dict, List, Type
from backtesting_engine.engine import BacktestingEngine
from backtesting_engine.strategies.base_strategy import Strategy

class StrategyOptimizer:
    """
    Optimizer engine that runs a grid search over specified parameter ranges
    to find the most optimal mathematical parameters for a given strategy.
    """
    
    def __init__(self, engine_kwargs: dict = None):
        """
        Initialize the Optimizer.
        
        Args:
            engine_kwargs: Shared kwargs for the BacktestingEngine instances 
                           (e.g. initial_capital, commission)
        """
        self.engine_kwargs = engine_kwargs or {}
        
    def optimize(self, 
                 strategy_class: Type[Strategy], 
                 data: pd.DataFrame, 
                 param_grid: Dict[str, List[any]],
                 metric: str = 'sharpe_ratio') -> pd.DataFrame:
        """
        Execute parameter sweep over all combinations in param_grid.
        
        Args:
            strategy_class: The class of the Strategy to test (e.g. RSIStrategy)
            data: Historic market data DataFrame
            param_grid: Dictionary mapping parameter names to lists of values to test
            metric: The target metric to maximize (e.g., 'sharpe_ratio', 'total_return')
            
        Returns:
            DataFrame containing the results of all combinations, sorted by the target metric.
        """
        
        # Generate all combinations of parameters
        keys, values = zip(*param_grid.items())
        combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
        
        results = []
        
        for params in combinations:
            try:
                # Instantiate strategy with current param combination
                strategy = strategy_class(**params)
                
                # Setup isolated engine
                engine = BacktestingEngine(**self.engine_kwargs)
                engine.add_data(data)
                engine.add_strategy(strategy)
                
                # Run backtest
                engine.run_backtest(strategy_name=strategy.name)
                metrics = engine.get_metrics(strategy_name=strategy.name)
                
                # Store row data
                row = params.copy()
                row['strategy_name'] = strategy.name
                row['total_return'] = metrics.get('total_return', 0)
                row['sharpe_ratio'] = metrics.get('sharpe_ratio', 0)
                row['max_drawdown'] = metrics.get('max_drawdown', 0)
                row['win_rate'] = metrics.get('win_rate', 0)
                
                results.append(row)
            except Exception as e:
                # Log or handle failure for this specific combo (e.g., invalid param pairings)
                print(f"Failed combination {params}: {e}")
                
        results_df = pd.DataFrame(results)
        if not results_df.empty and metric in results_df.columns:
            results_df = results_df.sort_values(by=metric, ascending=False).reset_index(drop=True)
            
        return results_df
