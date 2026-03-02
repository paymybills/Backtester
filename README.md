# Backtesting Engine

A flexible and powerful backtesting framework for testing trading strategies on historical market data with both Python API and modern web interface.

## Features

- **Multi-Source Data Integration**: Load market data from CSV, SQL, or generate synthetic data
- **Strategy Definition & Execution**: Easily define and test trading strategies
- **Realistic Trading Simulation**: Account for commissions, slippage, and other real-world trading constraints
- **Comprehensive Performance Analysis**: Calculate key performance metrics (Sharpe ratio, drawdown, etc.)
- **Professional Reporting & Visualization**: Generate interactive charts and HTML reports
- **Modern Web Interface**: React-based UI implementing professional Figma designs
- **RESTful API**: FastAPI backend for web integration and external applications

## Quick Start

### Option 1: Web Interface (Recommended)
```bash
# Navigate to the UI directory
cd ui/

# Install dependencies and start the web application
./start.sh

# Open http://localhost:8000 in your browser
```

### Option 2: Python API
```bash
# Install the package
pip install -e .

# Use in your Python code
from backtesting_engine import (
    DataIngestion, 
    MovingAverageCrossover,
    BacktestingEngine,
    Reporting
)

# Generate or load data
data_source = DataIngestion()
data = data_source.generate_sample_data(
    start_date='2020-01-01',
    end_date='2024-01-01'
)

# Create a strategy
ma_strategy = MovingAverageCrossover(short_window=50, long_window=200)

# Set up and run the backtest
engine = BacktestingEngine(initial_capital=100000.0)
engine.add_data(data)
engine.add_strategy(ma_strategy)
results = engine.run_backtest()

# Get performance metrics
metrics = engine.get_metrics(ma_strategy.name)
print(f"Total Return: {metrics['total_return']*100:.2f}%")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")

# Generate visualizations
reporter = Reporting()
portfolio = results[ma_strategy.name]['portfolio']
reporter.plot_equity_curve(portfolio).show()
```

## Web Interface

The web interface provides a professional, modern UI for the backtesting engine:

### Dashboard
- Real-time KPI metrics and performance indicators
- Recent backtests overview with status tracking
- Interactive charts and data visualization

### Strategy Configuration
- Visual strategy builder with form-based configuration
- Support for popular technical indicators (MA, RSI, etc.)
- Custom strategy code editor for advanced users

### Backtest Execution
- Interactive controls for running backtests
- Real-time progress tracking and status updates
- Parameter configuration (capital, commissions, dates)

### Results & Reports
- Comprehensive performance analysis
- Interactive equity curves and return distributions
- Detailed trade history and metrics comparison
- Export functionality (CSV, PDF)

### Screenshots
![Dashboard](ui/screenshots/dashboard.png)
![Strategy Config](ui/screenshots/strategy-config.png)
![Backtest Execution](ui/screenshots/execution.png)
![Results Report](ui/screenshots/results.png)

## Architecture

```
backtesting_engine/
├── backtesting_engine/     # Core Python package
│   ├── data/              # Data ingestion and processing
│   ├── strategies/        # Trading strategy implementations
│   ├── visualization/     # Charts and reporting
│   ├── engine.py          # Main backtesting engine
│   ├── metrics.py         # Performance metrics
│   └── simulation.py      # Trade simulation
├── ui/                    # Web interface
│   ├── src/              # React frontend
│   ├── backend.py        # FastAPI backend
│   ├── server.py         # Combined server
│   └── requirements.txt  # Python web dependencies
├── examples/             # Usage examples
├── tests/               # Unit tests
└── requirements.txt     # Core package dependencies
```

## Available Strategies

The package includes several built-in strategies:

1. **Moving Average Crossover**: Generates signals based on the crossing of short and long-term moving averages
2. **RSI (Relative Strength Index)**: Generates signals based on overbought/oversold conditions

You can also create custom strategies by extending the `Strategy` base class.

## Creating Custom Strategies

```python
from backtesting_engine import Strategy
import pandas as pd

class MyCustomStrategy(Strategy):
    def __init__(self, param1=10, param2=20):
        super().__init__(name="MyStrategy")
        self.param1 = param1
        self.param2 = param2
    
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['close']
        
        # Your custom signal logic here
        # ...
        
        self.signals = signals
        return signals
```

## Examples

See the `examples` directory for complete examples:

- `ma_crossover_example.py`: Basic moving average crossover strategy
- `strategy_comparison_example.py`: Compare multiple strategies on the same data

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.