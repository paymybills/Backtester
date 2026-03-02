"""
Performance metrics module for evaluating trading strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Union

class Metrics:
    """
    Class for calculating performance metrics of trading strategies.
    """
    
    def __init__(self, portfolio: pd.DataFrame, benchmark: Optional[pd.Series] = None):
        """
        Initialize the Metrics class.
        
        Args:
            portfolio: DataFrame with portfolio values and returns
            benchmark: Series with benchmark prices for comparison
        """
        self.portfolio = portfolio
        self.benchmark = benchmark
        
        # Calculate benchmark returns if provided
        if benchmark is not None:
            self.benchmark_returns = benchmark.pct_change().dropna()
        else:
            self.benchmark_returns = None
    
    def calculate_metrics(self) -> Dict[str, float]:
        """
        Calculate all performance metrics.
        
        Returns:
            Dictionary with calculated metrics
        """
        metrics = {}
        
        # Ensure we have the required columns
        required_cols = ['total', 'daily_returns']
        for col in required_cols:
            if col not in self.portfolio.columns:
                raise ValueError(f"Required column {col} not found in portfolio DataFrame")
        
        # Total return
        initial_value = self.portfolio['total'].iloc[0]
        final_value = self.portfolio['total'].iloc[-1]
        total_return = (final_value - initial_value) / initial_value
        metrics['total_return'] = total_return
        
        # Annualized return
        days = (self.portfolio.index[-1] - self.portfolio.index[0]).days
        years = days / 365.25
        metrics['annualized_return'] = (1 + total_return) ** (1 / years) - 1
        
        # Daily returns stats
        returns = self.portfolio['daily_returns'].dropna()
        metrics['daily_mean'] = returns.mean()
        metrics['daily_std'] = returns.std()
        
        # Sharpe ratio (assuming risk-free rate of 0 for simplicity)
        risk_free_rate = 0.0  # Can be parameterized later
        sharpe_ratio = (metrics['annualized_return'] - risk_free_rate) / (metrics['daily_std'] * np.sqrt(252))
        metrics['sharpe_ratio'] = sharpe_ratio
        
        # Sortino ratio (downside risk only)
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std()
        metrics['sortino_ratio'] = (metrics['annualized_return'] - risk_free_rate) / (downside_std * np.sqrt(252)) if not pd.isna(downside_std) and downside_std != 0 else np.nan
        
        # Maximum drawdown
        if 'drawdown' not in self.portfolio.columns:
            max_value = self.portfolio['total'].cummax()
            drawdown = (self.portfolio['total'] - max_value) / max_value
            metrics['max_drawdown'] = drawdown.min()
        else:
            metrics['max_drawdown'] = self.portfolio['drawdown'].min()
        
        # Calmar ratio
        metrics['calmar_ratio'] = metrics['annualized_return'] / abs(metrics['max_drawdown']) if metrics['max_drawdown'] != 0 else np.nan
        
        # Winning days
        metrics['winning_days'] = (returns > 0).sum() / len(returns)
        
        # Average win/loss
        metrics['avg_win'] = returns[returns > 0].mean() if len(returns[returns > 0]) > 0 else 0
        metrics['avg_loss'] = returns[returns < 0].mean() if len(returns[returns < 0]) > 0 else 0
        
        # Win/loss ratio
        metrics['win_loss_ratio'] = abs(metrics['avg_win'] / metrics['avg_loss']) if metrics['avg_loss'] != 0 else np.nan
        
        # Benchmark comparison if benchmark is provided
        if self.benchmark_returns is not None:
            # Align portfolio returns with benchmark returns
            aligned_returns = returns.reindex(self.benchmark_returns.index).dropna()
            aligned_benchmark = self.benchmark_returns.reindex(aligned_returns.index).dropna()
            
            if len(aligned_returns) > 0 and len(aligned_benchmark) > 0:
                # Beta
                cov_matrix = np.cov(aligned_returns, aligned_benchmark)
                if cov_matrix.shape == (2, 2) and cov_matrix[1, 1] != 0:
                    metrics['beta'] = cov_matrix[0, 1] / cov_matrix[1, 1]
                else:
                    metrics['beta'] = np.nan
                
                # Alpha (Jensen's Alpha)
                rf_daily = risk_free_rate / 252  # Daily risk-free rate
                metrics['alpha'] = (metrics['daily_mean'] - rf_daily) - metrics['beta'] * (aligned_benchmark.mean() - rf_daily)
                
                # Information ratio
                tracking_error = (aligned_returns - aligned_benchmark).std() * np.sqrt(252)
                metrics['information_ratio'] = (metrics['annualized_return'] - (aligned_benchmark.mean() * 252)) / tracking_error if tracking_error != 0 else np.nan
                
                # R-squared
                metrics['r_squared'] = np.corrcoef(aligned_returns, aligned_benchmark)[0, 1] ** 2
        
        return metrics
    
    def drawdown_periods(self, threshold: float = -0.05) -> pd.DataFrame:
        """
        Identify drawdown periods exceeding a threshold.
        
        Args:
            threshold: Drawdown threshold to identify significant drawdowns
            
        Returns:
            DataFrame with drawdown periods
        """
        if 'drawdown' not in self.portfolio.columns:
            max_value = self.portfolio['total'].cummax()
            drawdown = (self.portfolio['total'] - max_value) / max_value
            self.portfolio['drawdown'] = drawdown
        
        drawdown = self.portfolio['drawdown']
        
        # Identify periods where drawdown exceeds threshold
        exceed_threshold = drawdown < threshold
        
        # Find start and end of drawdown periods
        exceed_changes = exceed_threshold.astype(int).diff()
        starts = self.portfolio.index[exceed_changes == 1].tolist()
        ends = self.portfolio.index[exceed_changes == -1].tolist()
        
        # Handle case where we're still in a drawdown at the end
        if len(starts) > len(ends):
            ends.append(self.portfolio.index[-1])
        
        # Create DataFrame with drawdown periods
        periods = []
        for start, end in zip(starts, ends):
            period_dd = drawdown.loc[start:end]
            periods.append({
                'start': start,
                'end': end,
                'duration_days': (end - start).days,
                'max_drawdown': period_dd.min(),
                'recovery_days': None if end == self.portfolio.index[-1] and drawdown.iloc[-1] < threshold else (end - start).days
            })
        
        return pd.DataFrame(periods)