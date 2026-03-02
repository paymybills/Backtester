#!/bin/bash

# Backtesting Engine Web Application Startup Script

echo "🚀 Starting Backtesting Engine Web Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build the frontend
echo "🔨 Building React frontend..."
npm run build

# Start the combined server
echo "🌐 Starting web server on http://localhost:8000..."
python server.py