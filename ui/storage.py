"""
Simple file-based storage for strategies and backtests.
In production, replace this with a proper database (PostgreSQL, MongoDB, etc.)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class Storage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.strategies_file = self.data_dir / "strategies.json"
        self.backtests_file = self.data_dir / "backtests.json"
        
        # Initialize files if they don't exist
        if not self.strategies_file.exists():
            self._write_json(self.strategies_file, [])
        if not self.backtests_file.exists():
            self._write_json(self.backtests_file, [])
    
    def _read_json(self, filepath: Path) -> Any:
        """Read JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def _write_json(self, filepath: Path, data: Any):
        """Write JSON file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    # Strategy operations
    def save_strategy(self, strategy_data: Dict) -> Dict:
        """Save a new strategy."""
        strategies = self._read_json(self.strategies_file)
        
        # Add metadata
        strategy_id = f"strat_{len(strategies) + 1:03d}"
        strategy_data["id"] = strategy_id
        strategy_data["created_at"] = datetime.utcnow().isoformat()
        strategy_data["updated_at"] = datetime.utcnow().isoformat()
        
        strategies.append(strategy_data)
        self._write_json(self.strategies_file, strategies)
        
        return strategy_data
    
    def get_strategies(self) -> List[Dict]:
        """Get all strategies."""
        return self._read_json(self.strategies_file)
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict]:
        """Get a specific strategy by ID."""
        strategies = self._read_json(self.strategies_file)
        for strategy in strategies:
            if strategy.get("id") == strategy_id:
                return strategy
        return None
    
    def update_strategy(self, strategy_id: str, updates: Dict) -> Optional[Dict]:
        """Update an existing strategy."""
        strategies = self._read_json(self.strategies_file)
        
        for i, strategy in enumerate(strategies):
            if strategy.get("id") == strategy_id:
                strategy.update(updates)
                strategy["updated_at"] = datetime.utcnow().isoformat()
                strategies[i] = strategy
                self._write_json(self.strategies_file, strategies)
                return strategy
        
        return None
    
    def delete_strategy(self, strategy_id: str) -> bool:
        """Delete a strategy."""
        strategies = self._read_json(self.strategies_file)
        original_count = len(strategies)
        
        strategies = [s for s in strategies if s.get("id") != strategy_id]
        
        if len(strategies) < original_count:
            self._write_json(self.strategies_file, strategies)
            return True
        return False
    
    # Backtest operations
    def save_backtest_result(self, backtest_data: Dict) -> Dict:
        """Save backtest results."""
        backtests = self._read_json(self.backtests_file)
        
        # Add metadata if not present
        if "id" not in backtest_data:
            backtest_data["id"] = f"bt_{len(backtests) + 1:03d}"
        if "saved_at" not in backtest_data:
            backtest_data["saved_at"] = datetime.utcnow().isoformat()
        
        backtests.append(backtest_data)
        self._write_json(self.backtests_file, backtests)
        
        return backtest_data
    
    def get_backtests(self, limit: Optional[int] = None) -> List[Dict]:
        """Get all backtests, optionally limited to most recent."""
        backtests = self._read_json(self.backtests_file)
        
        # Sort by saved_at descending (most recent first)
        backtests.sort(key=lambda x: x.get("saved_at", ""), reverse=True)
        
        if limit:
            return backtests[:limit]
        return backtests
    
    def get_backtest(self, backtest_id: str) -> Optional[Dict]:
        """Get a specific backtest by ID."""
        backtests = self._read_json(self.backtests_file)
        for backtest in backtests:
            if backtest.get("id") == backtest_id:
                return backtest
        return None
    
    def delete_backtest(self, backtest_id: str) -> bool:
        """Delete a backtest."""
        backtests = self._read_json(self.backtests_file)
        original_count = len(backtests)
        
        backtests = [b for b in backtests if b.get("id") != backtest_id]
        
        if len(backtests) < original_count:
            self._write_json(self.backtests_file, backtests)
            return True
        return False
    
    # Statistics
    def get_stats(self) -> Dict:
        """Get dashboard statistics."""
        strategies = self.get_strategies()
        backtests = self.get_backtests()
        
        # Calculate real statistics
        total_strategies = len(strategies)
        
        # Count running backtests (those saved in last hour without completed status)
        active_backtests = sum(1 for bt in backtests 
                              if bt.get("status") == "running")
        
        # Calculate average Sharpe ratio from completed backtests
        sharpe_ratios = [
            bt.get("metrics", {}).get("sharpe_ratio", 0) 
            for bt in backtests 
            if bt.get("status") == "completed" and bt.get("metrics") and bt.get("metrics", {}).get("sharpe_ratio") is not None
        ]
        avg_sharpe = sum(sharpe_ratios) / len(sharpe_ratios) if sharpe_ratios else 0.0
        
        # Find best ROI
        rois = [
            bt.get("metrics", {}).get("total_return", 0) 
            for bt in backtests 
            if bt.get("status") == "completed" and bt.get("metrics") and bt.get("metrics", {}).get("total_return") is not None
        ]
        best_roi = max(rois) if rois else 0.0
        
        return {
            "total_strategies": total_strategies,
            "active_backtests": active_backtests,
            "avg_sharpe_ratio": round(avg_sharpe, 2),
            "best_strategy_roi": round(best_roi, 1)
        }
