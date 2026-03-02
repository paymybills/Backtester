#!/bin/bash
# Backtesting Engine Stop Script

echo "🛑 Stopping Backtesting Engine..."
echo "=================================="

# Kill backend
echo "Stopping backend..."
pkill -9 -f 'python.*ui/backend.py'
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Kill frontend
echo "Stopping frontend..."
pkill -9 -f 'vite'
lsof -ti:3001,3000 | xargs kill -9 2>/dev/null

sleep 1

echo ""
echo "✅ All servers stopped!"
