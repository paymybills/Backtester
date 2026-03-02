#!/bin/bash
# Backtesting Engine Startup Script

echo "🚀 Starting Backtesting Engine..."
echo "=================================="

# Kill any existing processes on ports 8000 and 3001
echo "Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Wait for ports to free up
sleep 2

# Start backend in background
echo "Starting backend server..."
cd /home/moew/Documents/BacktestingEngine
/home/moew/Documents/BacktestingEngine/.venv/bin/python ui/backend.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend server..."
cd /home/moew/Documents/BacktestingEngine/ui
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait a moment
sleep 2

echo ""
echo "✅ Servers Started Successfully!"
echo "=================================="
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3001 (or 3000)"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  Backend:  tail -f /home/moew/Documents/BacktestingEngine/backend.log"
echo "  Frontend: tail -f /home/moew/Documents/BacktestingEngine/ui/frontend.log"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
echo "Or run: pkill -f 'python.*ui/backend.py' && pkill -f 'vite'"
echo ""
