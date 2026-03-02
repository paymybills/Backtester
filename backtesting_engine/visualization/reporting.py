"""
Reporting and visualization module for backtesting results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, List, Optional, Tuple, Union
import os
import io

class Reporting:
    """
    Class for generating reports and visualizations of backtesting results.
    """
    
    def __init__(self):
        """Initialize the Reporting class."""
        # Set Matplotlib style
        plt.style.use('seaborn-v0_8-whitegrid')
    
    def plot_equity_curve(self, portfolio: pd.DataFrame, title: str = "Equity Curve", 
                         figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Plot the equity curve of a strategy.
        
        Args:
            portfolio: DataFrame with portfolio values
            title: Plot title
            figsize: Figure size
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Ensure we have the required columns
        if 'total' not in portfolio.columns:
            raise ValueError("Portfolio DataFrame must contain 'total' column")
        
        # Plot equity curve
        ax.plot(portfolio.index, portfolio['total'], linewidth=2, label='Portfolio Value')
        
        # Add drawdown as area if available
        if 'drawdown' not in portfolio.columns and 'peak' in portfolio.columns:
            portfolio['drawdown'] = (portfolio['total'] - portfolio['peak']) / portfolio['peak']
        
        if 'drawdown' in portfolio.columns:
            # Scale drawdown for better visibility
            max_drawdown = abs(portfolio['drawdown'].min())
            scaled_drawdown = portfolio['drawdown'] * (portfolio['total'].max() * 0.3) / max_drawdown
            
            # Plot drawdown as filled area
            ax.fill_between(
                portfolio.index,
                portfolio['total'].min(),
                portfolio['total'].min() + scaled_drawdown,
                where=scaled_drawdown < 0,
                alpha=0.3,
                color='red',
                label='Drawdown (scaled)'
            )
        
        # Format plot
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value', fontsize=12)
        ax.legend()
        ax.grid(True)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def plot_returns_distribution(self, portfolio: pd.DataFrame, 
                                title: str = "Returns Distribution",
                                figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Plot the distribution of returns.
        
        Args:
            portfolio: DataFrame with portfolio returns
            title: Plot title
            figsize: Figure size
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Ensure we have daily returns
        if 'daily_returns' not in portfolio.columns:
            portfolio['daily_returns'] = portfolio['total'].pct_change()
        
        returns = portfolio['daily_returns'].dropna()
        
        # Plot histogram
        n, bins, patches = ax.hist(
            returns, 
            bins=50, 
            alpha=0.7, 
            density=True, 
            color='blue',
            label='Daily Returns'
        )
        
        # Add normal distribution curve for comparison
        mu = returns.mean()
        sigma = returns.std()
        x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        ax.plot(x, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2)),
                linewidth=2, color='red', label='Normal Distribution')
        
        # Add mean and std lines
        ax.axvline(mu, color='green', linestyle='dashed', linewidth=2, label=f'Mean: {mu:.4f}')
        ax.axvline(0, color='black', linestyle='-', linewidth=1)
        
        # Format plot
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Daily Return', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend()
        ax.grid(True)
        
        plt.tight_layout()
        return fig
    
    def plot_drawdown_chart(self, portfolio: pd.DataFrame, 
                          title: str = "Drawdown Chart",
                          figsize: Tuple[int, int] = (12, 4)) -> plt.Figure:
        """
        Plot the drawdown chart of a strategy.
        
        Args:
            portfolio: DataFrame with portfolio values
            title: Plot title
            figsize: Figure size
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Ensure we have drawdown calculated
        if 'drawdown' not in portfolio.columns:
            if 'total' not in portfolio.columns:
                raise ValueError("Portfolio DataFrame must contain 'total' column")
            
            max_value = portfolio['total'].cummax()
            portfolio['drawdown'] = (portfolio['total'] - max_value) / max_value
        
        # Plot drawdown
        ax.fill_between(
            portfolio.index,
            0,
            portfolio['drawdown'],
            where=portfolio['drawdown'] < 0,
            alpha=0.8,
            color='red',
            label='Drawdown'
        )
        
        # Format plot
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Drawdown', fontsize=12)
        ax.legend()
        ax.grid(True)
        
        # Format y-axis as percentage
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def plot_strategy_comparison(self, portfolios: Dict[str, pd.DataFrame], 
                               benchmark: Optional[pd.Series] = None,
                               title: str = "Strategy Comparison",
                               figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Plot a comparison of multiple strategies.
        
        Args:
            portfolios: Dictionary of portfolio DataFrames for each strategy
            benchmark: Optional benchmark Series to include in comparison
            title: Plot title
            figsize: Figure size
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot each strategy
        for name, portfolio in portfolios.items():
            # Calculate cumulative returns if not available
            if 'cum_returns' not in portfolio.columns:
                if 'daily_returns' not in portfolio.columns:
                    portfolio['daily_returns'] = portfolio['total'].pct_change()
                portfolio['cum_returns'] = (1 + portfolio['daily_returns']).cumprod() - 1
            
            # Plot cumulative returns
            ax.plot(portfolio.index, portfolio['cum_returns'], linewidth=2, label=name)
        
        # Add benchmark if provided
        if benchmark is not None:
            benchmark_returns = benchmark.pct_change()
            benchmark_cum_returns = (1 + benchmark_returns).cumprod() - 1
            ax.plot(benchmark.index, benchmark_cum_returns, linewidth=2, linestyle='--', 
                   color='black', label='Benchmark')
        
        # Format plot
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Cumulative Returns', fontsize=12)
        ax.legend()
        ax.grid(True)
        
        # Format y-axis as percentage
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def generate_performance_summary(self, metrics: Dict[str, float]) -> str:
        """
        Generate a text summary of performance metrics.
        
        Args:
            metrics: Dictionary with performance metrics
            
        Returns:
            String with formatted performance summary
        """
        # Format metrics into a readable summary
        summary = []
        summary.append("Performance Summary")
        summary.append("=" * 40)
        
        # Total return
        summary.append(f"Total Return: {metrics.get('total_return', 0)*100:.2f}%")
        
        # Annualized return
        summary.append(f"Annualized Return: {metrics.get('annualized_return', 0)*100:.2f}%")
        
        # Risk metrics
        summary.append(f"Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}")
        summary.append(f"Sortino Ratio: {metrics.get('sortino_ratio', 0):.2f}")
        summary.append(f"Maximum Drawdown: {metrics.get('max_drawdown', 0)*100:.2f}%")
        summary.append(f"Calmar Ratio: {metrics.get('calmar_ratio', 0):.2f}")
        
        # Trading metrics
        summary.append(f"Winning Days: {metrics.get('winning_days', 0)*100:.2f}%")
        summary.append(f"Win/Loss Ratio: {metrics.get('win_loss_ratio', 0):.2f}")
        
        # Benchmark comparison
        if 'beta' in metrics:
            summary.append(f"Beta: {metrics.get('beta', 0):.2f}")
            summary.append(f"Alpha (annualized): {metrics.get('alpha', 0)*252*100:.2f}%")
            summary.append(f"R-Squared: {metrics.get('r_squared', 0):.2f}")
        
        return "\n".join(summary)
    
    def save_report_to_html(self, engine, output_path: str) -> str:
        """
        Generate and save a complete HTML report of the backtest results.
        
        Args:
            engine: BacktestingEngine instance with results
            output_path: Path to save the HTML report
            
        Returns:
            Path to the saved HTML file
        """
        from IPython.display import HTML
        import base64
        
        # Ensure the engine has results
        if not hasattr(engine, 'results') or not engine.results:
            raise ValueError("No backtest results found in engine")
        
        # Start building HTML content
        html_content = []
        html_content.append("<html><head>")
        html_content.append("<style>")
        html_content.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        html_content.append(".container { max-width: 1200px; margin: auto; }")
        html_content.append("h1, h2 { color: #333; }")
        html_content.append("table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }")
        html_content.append("table, th, td { border: 1px solid #ddd; }")
        html_content.append("th, td { padding: 8px; text-align: right; }")
        html_content.append("th { background-color: #f2f2f2; }")
        html_content.append("tr:nth-child(even) { background-color: #f9f9f9; }")
        html_content.append(".plot-container { margin: 20px 0; }")
        html_content.append("</style>")
        html_content.append("</head><body>")
        html_content.append("<div class='container'>")
        
        # Header
        html_content.append("<h1>Backtesting Report</h1>")
        html_content.append(f"<p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        # For each strategy
        for strategy_name, result in engine.results.items():
            html_content.append(f"<h2>Strategy: {strategy_name}</h2>")
            
            # Performance metrics
            metrics = engine.metrics.get(strategy_name, {})
            if metrics:
                html_content.append("<h3>Performance Metrics</h3>")
                html_content.append("<table>")
                html_content.append("<tr><th>Metric</th><th>Value</th></tr>")
                
                # Format metrics into table
                for key, value in metrics.items():
                    if isinstance(value, float):
                        if key.endswith('_return') or key == 'max_drawdown' or key.endswith('_days'):
                            formatted_value = f"{value*100:.2f}%"
                        else:
                            formatted_value = f"{value:.4f}"
                    else:
                        formatted_value = str(value)
                    
                    html_content.append(f"<tr><td>{key.replace('_', ' ').title()}</td><td>{formatted_value}</td></tr>")
                
                html_content.append("</table>")
            
            # Plots
            portfolio = result['portfolio']
            
            # Equity curve
            html_content.append("<h3>Equity Curve</h3>")
            fig = self.plot_equity_curve(portfolio, title=f"{strategy_name} - Equity Curve")
            img_data = self._fig_to_base64(fig)
            html_content.append(f"<div class='plot-container'><img src='data:image/png;base64,{img_data}' width='100%'></div>")
            plt.close(fig)
            
            # Drawdown chart
            html_content.append("<h3>Drawdown Chart</h3>")
            fig = self.plot_drawdown_chart(portfolio, title=f"{strategy_name} - Drawdown")
            img_data = self._fig_to_base64(fig)
            html_content.append(f"<div class='plot-container'><img src='data:image/png;base64,{img_data}' width='100%'></div>")
            plt.close(fig)
            
            # Returns distribution
            html_content.append("<h3>Returns Distribution</h3>")
            fig = self.plot_returns_distribution(portfolio, title=f"{strategy_name} - Returns Distribution")
            img_data = self._fig_to_base64(fig)
            html_content.append(f"<div class='plot-container'><img src='data:image/png;base64,{img_data}' width='100%'></div>")
            plt.close(fig)
        
        # Strategy comparison if multiple strategies
        if len(engine.results) > 1:
            html_content.append("<h2>Strategy Comparison</h2>")
            
            # Portfolio comparison plot
            portfolios = {name: result['portfolio'] for name, result in engine.results.items()}
            fig = self.plot_strategy_comparison(portfolios, title="Strategy Comparison")
            img_data = self._fig_to_base64(fig)
            html_content.append(f"<div class='plot-container'><img src='data:image/png;base64,{img_data}' width='100%'></div>")
            plt.close(fig)
            
            # Metrics comparison table
            html_content.append("<h3>Metrics Comparison</h3>")
            html_content.append("<table>")
            
            # Table headers
            metrics_keys = list(engine.metrics[next(iter(engine.metrics))].keys())
            html_content.append("<tr><th>Metric</th>")
            for name in engine.metrics.keys():
                html_content.append(f"<th>{name}</th>")
            html_content.append("</tr>")
            
            # Table rows
            for key in metrics_keys:
                html_content.append(f"<tr><td>{key.replace('_', ' ').title()}</td>")
                for name, metrics in engine.metrics.items():
                    value = metrics.get(key, "")
                    if isinstance(value, float):
                        if key.endswith('_return') or key == 'max_drawdown' or key.endswith('_days'):
                            formatted_value = f"{value*100:.2f}%"
                        else:
                            formatted_value = f"{value:.4f}"
                    else:
                        formatted_value = str(value)
                    
                    html_content.append(f"<td>{formatted_value}</td>")
                html_content.append("</tr>")
            
            html_content.append("</table>")
        
        # Close HTML
        html_content.append("</div></body></html>")
        
        # Save to file
        with open(output_path, 'w') as f:
            f.write("\n".join(html_content))
        
        return output_path
    
    def _fig_to_base64(self, fig: plt.Figure) -> str:
        """Convert a matplotlib figure to base64 string for HTML embedding."""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        import base64
        img_str = base64.b64encode(buf.read()).decode()
        buf.close()
        return img_str