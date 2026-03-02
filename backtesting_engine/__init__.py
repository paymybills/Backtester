"""
Backtesting Engine: A framework for testing trading strategies.

This package provides tools for:
1. Multi-Source Data Integration
2. Strategy Definition & Execution 
3. Realistic Trading Simulation
4. Comprehensive Performance Analysis
5. Professional Reporting & Visualization
"""

from .data.data_ingestion import DataIngestion
from .strategies.base_strategy import Strategy
from .strategies.moving_average import MovingAverageCrossover
from .strategies.rsi_strategy import RSIStrategy
from .strategies.rsi import RSIStrategy as RSIStrategyV2
from .strategies.macd import MACDStrategy
from .strategies.bollinger_bands import BollingerBandsStrategy
from .strategies.ensemble import EnsembleStrategy
from .simulation import Simulation
from .metrics import Metrics
from .visualization.reporting import Reporting
from .engine import BacktestingEngine
from .optimizer import StrategyOptimizer

__version__ = "0.1.0"