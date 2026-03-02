"""
FastAPI backend for the backtesting engine web application.

To start the application:
    ./start.sh

Or manually:
    Terminal 1: cd /home/moew/Documents/BacktestingEngine && .venv/bin/python ui/backend.py
    Terminal 2: cd /home/moew/Documents/BacktestingEngine/ui && npm run dev

To stop the application:
    ./stop.sh
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import uuid
import asyncio

# Import our backtesting engine
import sys
import os

# Add parent directory to path to import backtesting_engine
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from backtesting_engine import (
    DataIngestion,
    MovingAverageCrossover,
    RSIStrategy,
    BacktestingEngine,
    Reporting
)
from backtesting_engine.optimizer import StrategyOptimizer

# Import storage from ui directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from storage import Storage

app = FastAPI(title="Backtesting Engine API", version="1.0.0")

# Initialize storage with absolute path
import os
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
storage = Storage(data_dir=data_dir)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state management
class BacktestManager:
    def __init__(self):
        self.engines = {}
        self.running_backtests = {}
        self.results = {}
        
    def get_engine(self, engine_id: str = "default") -> BacktestingEngine:
        if engine_id not in self.engines:
            self.engines[engine_id] = BacktestingEngine(initial_capital=100000.0)
        return self.engines[engine_id]

manager = BacktestManager()

# Pydantic models for API
class StrategyConfig(BaseModel):
    name: str
    description: str
    asset_class: str
    timeframe: str
    entry_signal: str
    exit_signal: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    position_size: float = 10.0
    custom_code: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = {}

class BacktestConfig(BaseModel):
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float = 100000.0
    commission: float = 0.001
    slippage: float = 0.0005
    data_source: str = "synthetic"
    ticker: Optional[str] = "AAPL"  # For Yahoo Finance
    timeframe: str = "1d"  # Data granularity: "1m", "5m", "15m", "1h", "1d", "1wk"

class BacktestStatus(BaseModel):
    id: str
    status: str  # "running", "completed", "failed", "paused"
    progress: float
    current_step: str
    estimated_time_remaining: Optional[str] = None

class OptimizerConfig(BaseModel):
    strategy_type: str
    param_grid: Dict[str, List[Any]]
    data_source: str = "synthetic"
    ticker: Optional[str] = "AAPL"
    start_date: str
    end_date: str
    timeframe: str = "1d"
    initial_capital: float = 100000.0

manager.running_optimizations = {}

# API Routes

@app.get("/")
async def root():
    return {"message": "Backtesting Engine API", "status": "running"}

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard KPI statistics."""
    return storage.get_stats()

@app.get("/api/dashboard/recent-backtests")
async def get_recent_backtests():
    """Get recent backtest results."""
    backtests = storage.get_backtests(limit=10)
    
    # Format for frontend
    formatted = []
    for bt in backtests:
        formatted.append({
            "id": bt.get("id", "N/A"),
            "strategy": bt.get("strategy_name", "Unknown"),
            "status": bt.get("status", "Unknown"),
            "duration": bt.get("duration", "N/A"),
            "sharpe": f"{bt.get('metrics', {}).get('sharpe_ratio', 0):.2f}" if bt.get("metrics") else "-",
            "roi": f"{bt.get('metrics', {}).get('total_return', 0):.1f}%" if bt.get("metrics") else "-",
            "created_at": bt.get("saved_at", bt.get("started_at", ""))
        })
    
    return formatted

@app.get("/api/strategies")
async def get_strategies():
    """Get list of available strategies."""
    strategies = storage.get_strategies()
    
    # Format for frontend
    formatted = []
    for s in strategies:
        formatted.append({
            "id": s.get("id"),
            "name": s.get("name"),
            "description": s.get("description", ""),
            "type": s.get("entry_signal", "Custom"),
            "asset_class": s.get("asset_class", ""),
            "timeframe": s.get("timeframe", ""),
            "created_at": s.get("created_at")
        })
    
    return formatted

@app.post("/api/strategies")
async def create_strategy(strategy: StrategyConfig):
    """Create a new trading strategy."""
    try:
        # Save to storage
        strategy_data = strategy.dict()
        saved_strategy = storage.save_strategy(strategy_data)
        
        # Also add to engine for immediate use
        from backtesting_engine.strategies.moving_average import MovingAverageCrossover
        from backtesting_engine.strategies.rsi import RSIStrategy
        from backtesting_engine.strategies.macd import MACDStrategy
        from backtesting_engine.strategies.bollinger_bands import BollingerBandsStrategy
        from backtesting_engine.strategies.ensemble import EnsembleStrategy
        
        # Create strategy based on type
        params = strategy.parameters or {}
        
        if strategy.entry_signal == "ma-crossover":
            new_strategy = MovingAverageCrossover(
                short_window=int(params.get('short_window', 10)), 
                long_window=int(params.get('long_window', 30))
            )
        elif strategy.entry_signal == "rsi":
            new_strategy = RSIStrategy(
                period=int(params.get('period', 14)),
                oversold=float(params.get('oversold', 30)),
                overbought=float(params.get('overbought', 70))
            )
        elif strategy.entry_signal == "macd":
            new_strategy = MACDStrategy(
                fast_period=int(params.get('fast_period', 12)),
                slow_period=int(params.get('slow_period', 26)),
                signal_period=int(params.get('signal_period', 9))
            )
        elif strategy.entry_signal == "bollinger-bands":
            new_strategy = BollingerBandsStrategy(
                period=int(params.get('period', 20)),
                num_std=float(params.get('num_std', 2.0))
            )
        elif strategy.entry_signal == "ensemble":
            new_strategy = EnsembleStrategy(
                buy_threshold=float(params.get('buy_threshold', 0.6)),
                sell_threshold=float(params.get('sell_threshold', -0.6))
            )
        else:
            # Default to basic MA crossover
            new_strategy = MovingAverageCrossover(short_window=10, long_window=30)
        
        # We need to explicitly name the strategy with the user's string so they can select it
        new_strategy.name = strategy.name
        
        engine.add_strategy(new_strategy)
        
        return {
            "message": "Strategy created successfully",
            "strategy_id": saved_strategy["id"],
            "strategy": saved_strategy
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/backtests/start")
async def start_backtest(config: BacktestConfig, background_tasks: BackgroundTasks):
    """Start a new backtest."""
    try:
        backtest_id = str(uuid.uuid4())
        
        # Initialize backtest status
        manager.running_backtests[backtest_id] = {
            "id": backtest_id,
            "status": "running",
            "progress": 0.0,
            "current_step": "Initializing backtest...",
            "config": config.dict(),
            "started_at": datetime.utcnow()
        }
        
        # Start backtest in background
        background_tasks.add_task(run_backtest_task, backtest_id, config)
        
        return {
            "backtest_id": backtest_id,
            "status": "started",
            "message": "Backtest started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def run_backtest_task(backtest_id: str, config: BacktestConfig):
    """Background task to run the backtest."""
    try:
        # Update progress
        manager.running_backtests[backtest_id]["current_step"] = "Loading data..."
        manager.running_backtests[backtest_id]["progress"] = 10.0
        
        # Generate or load data
        data_ingestion = DataIngestion()
        
        # Support multiple data sources
        if config.data_source == "yahoo":
            ticker = config.ticker or "AAPL"
            
            # Map frontend timeframe to Yahoo Finance interval format
            interval_map = {
                "1m": "1m",
                "5m": "5m",
                "15m": "15m",
                "1h": "1h",
                "1d": "1d",
                "1w": "1wk",
                "1mo": "1mo"
            }
            interval = interval_map.get(config.timeframe, "1d")
            
            # Validate date range for intraday data
            from datetime import datetime
            start = datetime.strptime(config.start_date, "%Y-%m-%d")
            end = datetime.strptime(config.end_date, "%Y-%m-%d")
            days_diff = (end - start).days
            
            # Yahoo Finance limitations
            if interval == "1m" and days_diff > 7:
                raise ValueError(f"1-minute data is limited to 7 days. Your range is {days_diff} days. Please reduce the date range or use a longer timeframe.")
            elif interval == "5m" and days_diff > 60:
                raise ValueError(f"5-minute data is limited to 60 days. Your range is {days_diff} days. Please reduce the date range or use a longer timeframe.")
            elif interval in ["15m", "1h"] and days_diff > 730:
                raise ValueError(f"{interval} data is limited to ~730 days (2 years). Your range is {days_diff} days. Please reduce the date range.")
            
            data = data_ingestion.load_from_yahoo(
                ticker=ticker,
                start_date=config.start_date,
                end_date=config.end_date,
                interval=interval  # Now uses the selected timeframe!
            )
            if data is None:
                raise ValueError(f"Failed to load data for {ticker} from Yahoo Finance. Try using daily (1d) timeframe for long date ranges.")
        else:
            # Default to synthetic data
            data = data_ingestion.generate_sample_data(
                start_date=config.start_date,
                end_date=config.end_date
            )
        
        # Update progress
        manager.running_backtests[backtest_id]["current_step"] = "Initializing strategy..."
        manager.running_backtests[backtest_id]["progress"] = 30.0
        await asyncio.sleep(1)  # Simulate processing time
        
        # Create engine and strategy
        engine = BacktestingEngine(initial_capital=config.initial_capital)
        
        # Add data to engine first
        engine.add_data(data)
        
        # In this endpoint, we load the actual strategy from the engine cache which was placed there during creation
        # Find the strategy by name from the main manager's engine cache.
        main_engine = manager.get_engine()
        if config.strategy_name in main_engine.strategies:
            # Re-instantiate the actual strategy instance instead of referencing it directly
            # For now, just copy the strategy object over
            strategy = main_engine.strategies[config.strategy_name]
        else:
            # Fallback
            from backtesting_engine.strategies.moving_average import MovingAverageCrossover
            strategy = MovingAverageCrossover(short_window=10, long_window=30)
            strategy.name = config.strategy_name
            
        engine.add_strategy(strategy)
        
        # Update progress
        manager.running_backtests[backtest_id]["current_step"] = "Running simulation..."
        manager.running_backtests[backtest_id]["progress"] = 50.0
        await asyncio.sleep(2)  # Simulate processing time
        
        # Run backtest (data already loaded into engine)
        results = engine.run_backtest(strategy_name=strategy.name)
        
        # Update progress
        manager.running_backtests[backtest_id]["current_step"] = "Calculating metrics..."
        manager.running_backtests[backtest_id]["progress"] = 80.0
        await asyncio.sleep(1)
        
        # Calculate metrics
        strategy_name = list(results.keys())[0]
        metrics = results[strategy_name]["metrics"]
        portfolio = results[strategy_name]["portfolio"]
        
        # Convert portfolio to JSON-serializable format with NaN handling
        portfolio_data = []
        for date, row in portfolio.iterrows():
            portfolio_data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "total": float(np.nan_to_num(row.get("total", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "daily_returns": float(np.nan_to_num(row.get("daily_returns", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "cum_returns": float(np.nan_to_num(row.get("cum_returns", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "cash": float(np.nan_to_num(row.get("cash", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "holdings": float(np.nan_to_num(row.get("holdings", 0), nan=0.0, posinf=0.0, neginf=0.0))
            })
        
        # Extract trades from portfolio (where positions change) and calculate proper PnL
        trades_data = []
        winning_trades = 0
        total_completed_trades = 0
        
        if "portfolio" in results[strategy_name]:
            portfolio_df = results[strategy_name]["portfolio"]
            
            # Find where positions change (actual trades)
            if 'positions' in portfolio_df.columns:
                position_changes = portfolio_df['positions'].fillna(0).diff()
                trade_rows = portfolio_df[position_changes != 0]
                
                # Get ticker from config or default to "ASSET"
                ticker = config.ticker if config.data_source == "yahoo" else "ASSET"
                
                # Track buy/sell pairs to calculate actual PnL
                buy_price = None
                buy_date = None
                
                for i, (date, row) in enumerate(trade_rows.iterrows()):
                    position_change = position_changes.loc[date]
                    current_price = row.get("price", 0)
                    
                    # Determine trade side and calculate PnL
                    if position_change > 0:
                        side = "BUY"
                        buy_price = current_price
                        buy_date = date
                        pnl = 0.0  # No PnL on entry
                    elif position_change < 0:
                        side = "SELL"
                        # Calculate PnL from the buy-sell pair
                        if buy_price is not None and buy_price > 0:
                            pnl = ((current_price - buy_price) / buy_price) * 100
                            
                            # Track winning vs losing trades
                            total_completed_trades += 1
                            if pnl > 0:
                                winning_trades += 1
                        else:
                            pnl = 0.0
                        
                        buy_price = None  # Reset for next trade
                        buy_date = None
                    else:
                        continue  # Skip if no actual change
                    
                    trades_data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "ticker": ticker,
                        "side": side,
                        "quantity": abs(int(row.get("holdings", 0) / row.get("price", 1))) if row.get("price", 0) > 0 else 0,
                        "price": float(np.nan_to_num(current_price, nan=0.0, posinf=0.0, neginf=0.0)),
                        "pnl": float(np.nan_to_num(pnl, nan=0.0, posinf=0.0, neginf=0.0))
                    })
        
        # Calculate proper trade-based win rate
        trade_win_rate = (winning_trades / total_completed_trades * 100) if total_completed_trades > 0 else 0.0
        
        # Store results in memory
        manager.results[backtest_id] = {
            "config": config.dict(),
            "results": results,
            "engine": engine,
            "completed_at": datetime.utcnow()
        }
        
        # Also save to persistent storage with full data and NaN handling
        backtest_record = {
            "id": backtest_id,
            "strategy_name": config.strategy_name,
            "status": "completed",
            "started_at": manager.running_backtests[backtest_id]["started_at"].isoformat(),
            "completed_at": datetime.utcnow().isoformat(),
            "duration": str(datetime.utcnow() - manager.running_backtests[backtest_id]["started_at"]),
            "config": config.dict(),
            "metrics": {
                "total_return": float(np.nan_to_num(metrics.get("total_return", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "annualized_return": float(np.nan_to_num(metrics.get("annualized_return", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "sharpe_ratio": float(np.nan_to_num(metrics.get("sharpe_ratio", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "sortino_ratio": float(np.nan_to_num(metrics.get("sortino_ratio", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "max_drawdown": float(np.nan_to_num(metrics.get("max_drawdown", 0), nan=0.0, posinf=0.0, neginf=0.0)),
                "winning_days": float(metrics.get("winning_days", 0)),
                "trade_win_rate": float(trade_win_rate),  # Proper trade-based win rate
                "total_trades": len(trades_data)
            },
            "portfolio_data": portfolio_data,
            "trades": trades_data
        }
        storage.save_backtest_result(backtest_record)
        
        # Update final status
        manager.running_backtests[backtest_id]["status"] = "completed"
        manager.running_backtests[backtest_id]["progress"] = 100.0
        manager.running_backtests[backtest_id]["current_step"] = "Backtest completed successfully"
        
    except Exception as e:
        manager.running_backtests[backtest_id]["status"] = "failed"
        manager.running_backtests[backtest_id]["current_step"] = f"Error: {str(e)}"

@app.get("/api/backtests/{backtest_id}/status")
async def get_backtest_status(backtest_id: str):
    """Get the status of a running backtest."""
    if backtest_id not in manager.running_backtests:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    status = manager.running_backtests[backtest_id]
    
    # Calculate estimated time remaining
    if status["status"] == "running" and status["progress"] > 0:
        elapsed = (datetime.utcnow() - status["started_at"]).total_seconds()
        estimated_total = elapsed / (status["progress"] / 100)
        remaining = estimated_total - elapsed
        estimated_time_remaining = f"{int(remaining // 60)}m {int(remaining % 60)}s"
    else:
        estimated_time_remaining = None
    
    return {
        "id": backtest_id,
        "status": status["status"],
        "progress": status["progress"],
        "current_step": status["current_step"],
        "estimated_time_remaining": estimated_time_remaining
    }

@app.get("/api/backtests/{backtest_id}/results")
async def get_backtest_results(backtest_id: str):
    """Get the results of a completed backtest."""
    if backtest_id not in manager.results:
        raise HTTPException(status_code=404, detail="Backtest results not found")
    
    result_data = manager.results[backtest_id]
    results = result_data["results"]
    
    # Extract metrics for the strategy
    strategy_name = list(results.keys())[0]
    metrics = results[strategy_name]["metrics"]
    portfolio = results[strategy_name]["portfolio"]
    
    # Convert portfolio to JSON-serializable format
    portfolio_data = []
    for date, row in portfolio.iterrows():
        portfolio_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "portfolio_value": float(row.get("total", 0)),
            "daily_return": float(row.get("daily_returns", 0)),
            "cumulative_return": float(row.get("cum_returns", 0))
        })
    
    # Format trades data (extract from signals where position changes)
    trades_data = []
    signals = results[strategy_name].get("signals", portfolio)
    if 'positions' in signals.columns:
        position_changes = signals['positions'].diff()
        trade_dates = signals.index[position_changes != 0]
        
        for i, date in enumerate(trade_dates[1:]):  # Skip first row
            row = signals.loc[date]
            trades_data.append({
                "id": f"T{i+1:03d}",
                "date": date.strftime("%Y-%m-%d"),
                "type": "BUY" if row['positions'] > 0 else "SELL",
                "price": float(row.get('price', 0)),
                "shares": 0,  # Would need to calculate from portfolio
                "commission": 0  # Would need to calculate
            })
    
    return {
        "backtest_id": backtest_id,
        "strategy_name": strategy_name,
        "metrics": {
            "total_return": float(metrics.get("total_return", 0)) * 100,
            "annualized_return": float(metrics.get("annualized_return", 0)) * 100,
            "sharpe_ratio": float(metrics.get("sharpe_ratio", 0)),
            "sortino_ratio": float(metrics.get("sortino_ratio", 0)),
            "max_drawdown": float(metrics.get("max_drawdown", 0)) * 100,
            "win_rate": float(metrics.get("trade_win_rate", metrics.get("winning_days", 0))) * 100 if metrics.get("trade_win_rate", 0) <= 1.0 else float(metrics.get("trade_win_rate", 0)),  # Handle both decimal and percentage formats
            "total_trades": len(trades_data)
        },
        "portfolio_data": portfolio_data,
        "trades": trades_data[-10:],  # Last 10 trades
        "completed_at": result_data["completed_at"].isoformat()
    }

@app.post("/api/backtests/{backtest_id}/pause")
async def pause_backtest(backtest_id: str):
    """Pause a running backtest."""
    if backtest_id not in manager.running_backtests:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    manager.running_backtests[backtest_id]["status"] = "paused"
    manager.running_backtests[backtest_id]["current_step"] = "Backtest paused by user"
    
    return {"message": "Backtest paused successfully"}

@app.post("/api/backtests/{backtest_id}/stop")
async def stop_backtest(backtest_id: str):
    """Stop a running backtest."""
    if backtest_id not in manager.running_backtests:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    manager.running_backtests[backtest_id]["status"] = "stopped"
    manager.running_backtests[backtest_id]["current_step"] = "Backtest stopped by user"
    
    return {"message": "Backtest stopped successfully"}

@app.get("/api/backtests")
async def get_all_backtests():
    """Get all backtests (running and completed from storage)."""
    import math
    
    def clean_nan_values(obj):
        """Recursively clean NaN and Inf values from nested structures."""
        if isinstance(obj, dict):
            return {k: clean_nan_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nan_values(item) for item in obj]
        elif isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return 0.0
            return obj
        else:
            return obj
    
    try:
        all_backtests = []
        
        # Add running backtests
        for bt_id, bt_data in manager.running_backtests.items():
            all_backtests.append({
                "id": bt_id,
                "status": bt_data["status"],
                "progress": bt_data["progress"],
                "started_at": bt_data["started_at"].isoformat(),
                "config": bt_data["config"]
            })
        
        # Get completed backtests from storage
        stored_backtests = storage.get_backtests()
        for bt in stored_backtests:
            # Skip if already in running list
            if bt["id"] not in [x["id"] for x in all_backtests]:
                # Clean up all NaN values recursively
                bt = clean_nan_values(bt)
                all_backtests.append(bt)
        
        return all_backtests
    except Exception as e:
        import traceback
        print(f"Error in get_all_backtests: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/backtests/{backtest_id}")
async def get_backtest_details(backtest_id: str):
    """Get full details of a specific backtest from storage."""
    import math
    
    def clean_nan_values(obj):
        """Recursively clean NaN and Inf values from nested structures."""
        if isinstance(obj, dict):
            return {k: clean_nan_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nan_values(item) for item in obj]
        elif isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return 0.0
            return obj
        else:
            return obj
    
    backtest = storage.get_backtest(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    # Clean up all NaN values recursively
    backtest = clean_nan_values(backtest)
    
    return backtest

@app.post("/api/optimize")
async def optimize_strategy(config: OptimizerConfig, background_tasks: BackgroundTasks):
    """Start a parameter sweep optimization."""
    try:
        opt_id = str(uuid.uuid4())
        
        manager.running_optimizations[opt_id] = {
            "id": opt_id,
            "status": "running",
            "progress": 0.0,
            "current_step": "Initializing optimizer...",
            "config": config.dict(),
            "started_at": datetime.utcnow(),
            "results": None
        }
        
        background_tasks.add_task(run_optimizer_task, opt_id, config)
        
        return {
            "optimization_id": opt_id,
            "status": "started",
            "message": "Optimization started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def run_optimizer_task(opt_id: str, config: OptimizerConfig):
    try:
        manager.running_optimizations[opt_id]["current_step"] = "Loading data..."
        manager.running_optimizations[opt_id]["progress"] = 10.0
        
        data_ingestion = DataIngestion()
        if config.data_source == "yahoo":
            ticker = config.ticker or "AAPL"
            interval_map = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "1d": "1d", "1w": "1wk"}
            interval = interval_map.get(config.timeframe, "1d")
            data = data_ingestion.load_from_yahoo(ticker=ticker, start_date=config.start_date, end_date=config.end_date, interval=interval)
        else:
            data = data_ingestion.generate_sample_data(start_date=config.start_date, end_date=config.end_date)
            
        manager.running_optimizations[opt_id]["current_step"] = "Running parameter sweep..."
        manager.running_optimizations[opt_id]["progress"] = 30.0
        
        from backtesting_engine.strategies.moving_average import MovingAverageCrossover
        from backtesting_engine.strategies.rsi import RSIStrategy
        from backtesting_engine.strategies.macd import MACDStrategy
        from backtesting_engine.strategies.bollinger_bands import BollingerBandsStrategy
        from backtesting_engine.strategies.ensemble import EnsembleStrategy
        
        strategy_class_map = {
            "ma-crossover": MovingAverageCrossover,
            "rsi": RSIStrategy,
            "macd": MACDStrategy,
            "bollinger-bands": BollingerBandsStrategy,
            "ensemble": EnsembleStrategy
        }
        
        strat_class = strategy_class_map.get(config.strategy_type, MovingAverageCrossover)
        
        optimizer = StrategyOptimizer(engine_kwargs={"initial_capital": config.initial_capital})
        
        # This blocks, but it's a background task. In a real app we'd run in executor.
        results_df = optimizer.optimize(
            strategy_class=strat_class,
            data=data,
            param_grid=config.param_grid,
            metric="sharpe_ratio"
        )
        
        manager.running_optimizations[opt_id]["progress"] = 90.0
        manager.running_optimizations[opt_id]["current_step"] = "Saving results..."
        
        # Convert results to dict
        import math
        def clean_nan(obj):
            if isinstance(obj, float):
                return 0.0 if math.isnan(obj) or math.isinf(obj) else obj
            return obj

        results_list = []
        if not results_df.empty:
            for _, row in results_df.iterrows():
                row_dict = {k: clean_nan(v) for k, v in row.to_dict().items()}
                results_list.append(row_dict)
                
        manager.running_optimizations[opt_id]["results"] = results_list
        manager.running_optimizations[opt_id]["status"] = "completed"
        manager.running_optimizations[opt_id]["progress"] = 100.0
        manager.running_optimizations[opt_id]["current_step"] = "Optimization completed"
        
    except Exception as e:
        manager.running_optimizations[opt_id]["status"] = "failed"
        manager.running_optimizations[opt_id]["current_step"] = f"Error: {str(e)}"

@app.get("/api/optimize/{opt_id}")
async def get_optimization_status(opt_id: str):
    if opt_id not in manager.running_optimizations:
        raise HTTPException(status_code=404, detail="Optimization not found")
    return manager.running_optimizations[opt_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)