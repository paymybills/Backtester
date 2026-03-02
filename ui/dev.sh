#!/bin/bash

# Development mode startup script

echo "🔧 Starting Backtesting Engine in Development Mode..."

# Start the FastAPI backend in the background
echo "🐍 Starting Python backend on port 8000..."
cd /home/moew/Documents/BacktestingEngine/ui
python backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start the React frontend development server
echo "⚛️  Starting React frontend on port 3000..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Development servers started!"
echo "📊 Backend API: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down development servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait