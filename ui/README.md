
# Backtesting Engine Web Application

This directory contains the web-based user interface for the backtesting engine, implementing the Figma wireframe designs.

## Architecture

- **Frontend**: React + TypeScript + Vite + shadcn/ui components
- **Backend**: FastAPI (Python) 
- **Integration**: RESTful API connecting React frontend to Python backtesting engine

## Project Structure

```
ui/
├── src/                    # React frontend source
│   ├── components/         # UI components from Figma designs
│   │   ├── Dashboard.tsx           # Main dashboard with KPIs
│   │   ├── StrategyConfiguration.tsx   # Strategy setup form
│   │   ├── BacktestExecution.tsx       # Backtest controls
│   │   ├── ReportScreen.tsx            # Results visualization
│   │   └── ui/             # shadcn/ui components
│   ├── App.tsx             # Main application
│   └── main.tsx            # Entry point
├── backend.py              # FastAPI backend with API endpoints
├── server.py               # Combined server (API + static files)
├── package.json            # Node.js dependencies
└── requirements.txt        # Python dependencies
```

## Features Implemented

### 1. Dashboard
- Real-time KPI metrics (Total Strategies, Active Backtests, Sharpe Ratio, ROI)
- Recent backtests table with status indicators
- Responsive grid layout with modern card design

### 2. Strategy Configuration
- Interactive form for creating trading strategies
- Strategy type selection (MA Crossover, RSI, Custom)
- Parameter configuration (stop loss, take profit, position sizing)
- Code editor for custom strategy logic

### 3. Backtest Execution
- Strategy selection and date range picker
- Capital and commission configuration
- Real-time progress tracking with status updates
- Start/pause/stop controls
- Live statistics during execution

### 4. Report Screen
- Comprehensive performance metrics comparison
- Interactive equity curve chart (Strategy vs Benchmark)
- Monthly returns bar chart
- Detailed trades table with P&L
- Export functionality (CSV, PDF)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Install Python dependencies
pip install fastapi uvicorn pydantic

# Or install from requirements
pip install -r requirements.txt

# Run the backend
python backend.py
```

### Frontend Setup
```bash
# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

### Full Application
```bash
# Build frontend
npm run build

# Run combined server (API + Frontend)
python server.py
```

## API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Get KPI statistics
- `GET /api/dashboard/recent-backtests` - Get recent backtest results

### Strategies
- `GET /api/strategies` - List available strategies
- `POST /api/strategies` - Create new strategy

### Backtesting
- `POST /api/backtests/start` - Start new backtest
- `GET /api/backtests/{id}/status` - Get backtest progress
- `GET /api/backtests/{id}/results` - Get completed results
- `POST /api/backtests/{id}/pause` - Pause running backtest
- `POST /api/backtests/{id}/stop` - Stop running backtest

## Design System

The UI follows the Figma wireframe designs with:
- **Color Scheme**: Dark theme with green accent (#00ff88)
- **Typography**: Clean, modern font stack
- **Components**: shadcn/ui for consistent design
- **Layout**: Responsive grid system
- **Animations**: Subtle transitions and loading states

## Integration with Python Engine

The web interface integrates seamlessly with the existing Python backtesting engine:

1. **Data Ingestion**: Web interface calls Python DataIngestion class
2. **Strategy Execution**: Frontend configuration creates Python Strategy objects
3. **Simulation**: BacktestingEngine runs in background with progress updates
4. **Results**: Python metrics and visualizations served to React frontend
5. **Real-time Updates**: WebSocket-style polling for live backtest status

## Development Notes

- Frontend components match the exact Figma designs
- API responses are formatted for easy frontend consumption
- Background task processing for long-running backtests
- Error handling and loading states throughout
- Responsive design for desktop and tablet use

## Next Steps

1. **Real Data Integration**: Connect to live market data APIs
2. **User Authentication**: Add login/signup functionality
3. **Strategy Marketplace**: Share and download strategies
4. **Advanced Visualizations**: More interactive charts
5. **Portfolio Optimization**: Multi-strategy portfolio analysis
6. **Deployment**: Production deployment configuration