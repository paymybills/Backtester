"""
Streamlit Web Application for Backtesting Engine
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta
import time

# Add the parent directory to the path to import our backtesting engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtesting_engine import (
    DataIngestion,
    MovingAverageCrossover,
    RSIStrategy,
    BacktestingEngine,
    Reporting
)

# Page configuration
st.set_page_config(
    page_title="Backtesting Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #0E1117;
        border: 1px solid #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00ff88;
    }
    .stSelectbox > div > div {
        background-color: #262730;
    }
    .strategy-card {
        background-color: #1E1E1E;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #262730;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'backtest_results' not in st.session_state:
    st.session_state.backtest_results = {}
if 'saved_strategies' not in st.session_state:
    st.session_state.saved_strategies = []

def main():
    st.title("📈 Backtesting Engine")
    st.markdown("### Professional Trading Strategy Analysis Platform")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["Dashboard", "Strategy Configuration", "Backtest Execution", "Results & Reports"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Strategy Configuration":
        show_strategy_configuration()
    elif page == "Backtest Execution":
        show_backtest_execution()
    elif page == "Results & Reports":
        show_results_reports()

def show_dashboard():
    """Dashboard page with KPIs and recent backtests"""
    
    st.header("📊 Dashboard")
    
    # KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Strategies",
            value=len(st.session_state.saved_strategies),
            delta=1 if len(st.session_state.saved_strategies) > 0 else None
        )
    
    with col2:
        active_backtests = len([r for r in st.session_state.backtest_results.values() if r.get('status') == 'completed'])
        st.metric(
            label="Completed Backtests", 
            value=active_backtests,
            delta=1 if active_backtests > 0 else None
        )
    
    with col3:
        if st.session_state.backtest_results:
            sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in st.session_state.backtest_results.values() if 'metrics' in r]
            avg_sharpe = np.mean(sharpe_ratios) if sharpe_ratios else 0
        else:
            avg_sharpe = 0
        st.metric(
            label="Avg Sharpe Ratio",
            value=f"{avg_sharpe:.2f}",
            delta=0.1 if avg_sharpe > 1 else None
        )
    
    with col4:
        if st.session_state.backtest_results:
            returns = [r['metrics']['total_return_pct'] for r in st.session_state.backtest_results.values() if 'metrics' in r]
            best_roi = max(returns) if returns else 0
        else:
            best_roi = 0
        st.metric(
            label="Best Strategy ROI",
            value=f"{best_roi:.1f}%",
            delta=f"+{best_roi:.1f}%" if best_roi > 0 else None
        )
    
    st.markdown("---")
    
    # Recent Backtests
    st.subheader("🔄 Recent Backtests")
    
    if st.session_state.backtest_results:
        # Create a DataFrame for recent backtests
        backtest_data = []
        for backtest_id, result in st.session_state.backtest_results.items():
            if 'metrics' in result:
                backtest_data.append({
                    'ID': backtest_id[:8] + '...',
                    'Strategy': result.get('strategy_name', 'Unknown'),
                    'Status': 'Completed',
                    'Total Return': f"{result['metrics']['total_return_pct']:.1f}%",
                    'Sharpe Ratio': f"{result['metrics']['sharpe_ratio']:.2f}",
                    'Max Drawdown': f"{result['metrics']['max_drawdown_pct']:.1f}%",
                    'Trades': result['metrics']['total_trades']
                })
        
        if backtest_data:
            df = pd.DataFrame(backtest_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No completed backtests yet. Run a backtest to see results here.")
    else:
        st.info("No backtests run yet. Go to 'Backtest Execution' to run your first backtest!")
    
    # Strategy Performance Chart
    if st.session_state.backtest_results:
        st.subheader("📈 Strategy Performance Overview")
        
        # Create performance comparison chart
        strategy_names = []
        returns = []
        sharpe_ratios = []
        
        for result in st.session_state.backtest_results.values():
            if 'metrics' in result:
                strategy_names.append(result.get('strategy_name', 'Unknown'))
                returns.append(result['metrics']['total_return_pct'])
                sharpe_ratios.append(result['metrics']['sharpe_ratio'])
        
        if strategy_names:
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Total Returns (%)', 'Sharpe Ratios'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Returns bar chart
            fig.add_trace(
                go.Bar(x=strategy_names, y=returns, name="Returns", marker_color="#00ff88"),
                row=1, col=1
            )
            
            # Sharpe ratio bar chart
            fig.add_trace(
                go.Bar(x=strategy_names, y=sharpe_ratios, name="Sharpe", marker_color="#ff6b6b"),
                row=1, col=2
            )
            
            fig.update_layout(
                height=400,
                showlegend=False,
                template="plotly_dark",
                title_text="Strategy Performance Comparison"
            )
            
            st.plotly_chart(fig, use_container_width=True)

def show_strategy_configuration():
    """Strategy configuration page"""
    
    st.header("⚙️ Strategy Configuration")
    
    # Strategy creation form
    with st.container():
        st.subheader("📝 Create New Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Basic Information**")
            strategy_name = st.text_input("Strategy Name", placeholder="e.g., Mean Reversion v2")
            description = st.text_area("Description", placeholder="Brief description of your strategy...")
            asset_class = st.selectbox("Asset Class", ["Stocks", "Forex", "Cryptocurrency", "Commodities"])
            timeframe = st.selectbox("Timeframe", ["1 Minute", "5 Minutes", "1 Hour", "1 Day", "1 Week"])
        
        with col2:
            st.markdown("**Technical Parameters**")
            entry_signal = st.selectbox(
                "Entry Signal", 
                ["RSI Oversold", "MA Crossover", "Bollinger Bands", "MACD Signal"]
            )
            exit_signal = st.selectbox(
                "Exit Signal",
                ["RSI Overbought", "Stop Loss", "Take Profit", "Time Based"]
            )
            
            col2a, col2b = st.columns(2)
            with col2a:
                stop_loss = st.number_input("Stop Loss (%)", min_value=0.0, max_value=50.0, value=5.0, step=0.1)
            with col2b:
                take_profit = st.number_input("Take Profit (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
            
            position_size = st.number_input("Position Size (%)", min_value=1.0, max_value=100.0, value=10.0, step=0.1)
        
        # Strategy Logic (Optional)
        st.markdown("**Strategy Logic (Python Code)**")
        custom_code = st.text_area(
            "Custom Strategy Code",
            placeholder="""def strategy_logic(data):
    # Your strategy implementation here
    # Example:
    rsi = calculate_rsi(data['close'], 14)
    
    # Entry condition
    if rsi < 30:
        return 'BUY'
    
    # Exit condition  
    elif rsi > 70:
        return 'SELL'
    
    return 'HOLD'""",
            height=200
        )
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("💾 Save Strategy", type="primary"):
                if strategy_name:
                    strategy_config = {
                        'name': strategy_name,
                        'description': description,
                        'asset_class': asset_class,
                        'timeframe': timeframe,
                        'entry_signal': entry_signal,
                        'exit_signal': exit_signal,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'position_size': position_size,
                        'custom_code': custom_code,
                        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.saved_strategies.append(strategy_config)
                    st.success(f"Strategy '{strategy_name}' saved successfully!")
                else:
                    st.error("Please enter a strategy name")
        
        with col2:
            if st.button("✅ Validate Strategy"):
                if strategy_name and entry_signal:
                    st.success("Strategy configuration is valid!")
                else:
                    st.error("Please fill in required fields: Strategy Name and Entry Signal")
    
    # Saved Strategies
    st.markdown("---")
    st.subheader("📋 Saved Strategies")
    
    if st.session_state.saved_strategies:
        for i, strategy in enumerate(st.session_state.saved_strategies):
            with st.expander(f"🎯 {strategy['name']} - {strategy['created_at']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {strategy['description']}")
                    st.write(f"**Asset Class:** {strategy['asset_class']}")
                    st.write(f"**Timeframe:** {strategy['timeframe']}")
                with col2:
                    st.write(f"**Entry Signal:** {strategy['entry_signal']}")
                    st.write(f"**Exit Signal:** {strategy['exit_signal']}")
                    st.write(f"**Stop Loss:** {strategy['stop_loss']}%")
                
                if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.saved_strategies.pop(i)
                    st.rerun()
    else:
        st.info("No saved strategies yet. Create your first strategy above!")

def show_backtest_execution():
    """Backtest execution page"""
    
    st.header("🚀 Backtest Execution")
    
    if not st.session_state.saved_strategies:
        st.warning("No strategies available. Please create a strategy first in the 'Strategy Configuration' page.")
        return
    
    # Backtest Configuration
    st.subheader("⚙️ Backtest Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Strategy Selection**")
        strategy_names = [s['name'] for s in st.session_state.saved_strategies]
        selected_strategy = st.selectbox("Select Strategy", strategy_names)
        
        st.markdown("**Date Range**")
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
        end_date = st.date_input("End Date", value=datetime.now())
        
        st.markdown("**Capital Settings**")
        initial_capital = st.number_input("Initial Capital ($)", min_value=1000, value=100000, step=1000)
    
    with col2:
        st.markdown("**Trading Settings**")
        commission = st.number_input("Commission per Trade", min_value=0.0, max_value=1.0, value=0.001, step=0.0001, format="%.4f")
        slippage = st.number_input("Slippage Factor", min_value=0.0, max_value=1.0, value=0.0005, step=0.0001, format="%.4f")
        
        st.markdown("**Data Source**")
        data_source = st.selectbox("Data Source", ["Synthetic Data", "CSV File", "Yahoo Finance"])
        
        if data_source == "CSV File":
            uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])
        elif data_source == "Yahoo Finance":
            ticker_symbol = st.text_input("Ticker Symbol", placeholder="e.g., AAPL, TSLA")
    
    # Run Backtest Button
    st.markdown("---")
    
    if st.button("🏃‍♂️ Run Backtest", type="primary", use_container_width=True):
        if selected_strategy:
            run_backtest(
                selected_strategy, start_date, end_date, initial_capital, 
                commission, slippage, data_source
            )
        else:
            st.error("Please select a strategy")
    
    # Running Backtests Status
    st.markdown("---")
    st.subheader("📊 Backtest Status")
    
    # Show any running or completed backtests
    if st.session_state.backtest_results:
        for backtest_id, result in st.session_state.backtest_results.items():
            status = result.get('status', 'unknown')
            strategy_name = result.get('strategy_name', 'Unknown')
            
            if status == 'running':
                with st.container():
                    st.write(f"🔄 **{strategy_name}** - Running...")
                    progress = result.get('progress', 0)
                    st.progress(progress / 100)
            elif status == 'completed':
                st.write(f"✅ **{strategy_name}** - Completed")
            elif status == 'failed':
                st.write(f"❌ **{strategy_name}** - Failed")

def run_backtest(strategy_name, start_date, end_date, initial_capital, commission, slippage, data_source):
    """Run a backtest with the given parameters"""
    
    # Create a unique backtest ID
    backtest_id = f"BT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Initialize progress
    st.session_state.backtest_results[backtest_id] = {
        'status': 'running',
        'strategy_name': strategy_name,
        'progress': 0
    }
    
    # Create progress bar and status
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Load Data
        status_text.text("Loading data...")
        progress_bar.progress(20)
        
        data_ingestion = DataIngestion()
        if data_source == "Synthetic Data":
            data = data_ingestion.generate_sample_data(
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
        else:
            # For now, use synthetic data
            data = data_ingestion.generate_sample_data(
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
        
        # Step 2: Initialize Strategy
        status_text.text("Initializing strategy...")
        progress_bar.progress(40)
        
        # Find the selected strategy configuration
        strategy_config = next(s for s in st.session_state.saved_strategies if s['name'] == strategy_name)
        
        # Create strategy based on type
        if strategy_config['entry_signal'] == "MA Crossover":
            strategy = MovingAverageCrossover(short_window=50, long_window=200)
        elif strategy_config['entry_signal'] == "RSI Oversold":
            strategy = RSIStrategy(period=14, oversold=30, overbought=70)
        else:
            # Default to MA crossover
            strategy = MovingAverageCrossover(short_window=50, long_window=200)
        
        # Step 3: Run Backtest
        status_text.text("Running backtest simulation...")
        progress_bar.progress(60)
        
        engine = BacktestingEngine(initial_capital=initial_capital)
        engine.add_strategy(strategy)
        
        results = engine.run_backtest(
            data=data,
            strategy_name=strategy.name,
            commission_per_trade=commission,
            slippage_factor=slippage
        )
        
        # Step 4: Process Results
        status_text.text("Processing results...")
        progress_bar.progress(80)
        
        # Extract results for the strategy
        strategy_results = results[strategy.name]
        metrics = strategy_results['metrics']
        portfolio = strategy_results['portfolio']
        trades = strategy_results['trades']
        
        # Step 5: Complete
        status_text.text("Backtest completed!")
        progress_bar.progress(100)
        
        # Store results
        st.session_state.backtest_results[backtest_id] = {
            'status': 'completed',
            'strategy_name': strategy_name,
            'backtest_id': backtest_id,
            'metrics': metrics,
            'portfolio': portfolio,
            'trades': trades,
            'config': strategy_config,
            'completed_at': datetime.now()
        }
        
        time.sleep(1)  # Brief pause to show completion
        st.success(f"Backtest completed successfully! Check the 'Results & Reports' page to view detailed results.")
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.session_state.backtest_results[backtest_id]['status'] = 'failed'
        st.error(f"Backtest failed: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def show_results_reports():
    """Results and reports page"""
    
    st.header("📈 Results & Reports")
    
    if not st.session_state.backtest_results:
        st.info("No backtest results available. Run a backtest first!")
        return
    
    # Filter to completed backtests
    completed_results = {k: v for k, v in st.session_state.backtest_results.items() 
                        if v.get('status') == 'completed' and 'metrics' in v}
    
    if not completed_results:
        st.info("No completed backtests found.")
        return
    
    # Select backtest to view
    backtest_ids = list(completed_results.keys())
    backtest_names = [f"{v['strategy_name']} ({k[:8]})" for k, v in completed_results.items()]
    
    selected_idx = st.selectbox("Select Backtest Result", range(len(backtest_names)), 
                               format_func=lambda x: backtest_names[x])
    
    selected_backtest_id = backtest_ids[selected_idx]
    result = completed_results[selected_backtest_id]
    
    # Display Results
    st.subheader(f"📊 Results: {result['strategy_name']}")
    
    # Key Metrics
    metrics = result['metrics']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Return", f"{metrics['total_return_pct']:.1f}%")
    with col2:
        st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
    with col3:
        st.metric("Max Drawdown", f"{metrics['max_drawdown_pct']:.1f}%")
    with col4:
        st.metric("Total Trades", metrics['total_trades'])
    
    # Additional metrics in expandable section
    with st.expander("📋 Detailed Metrics"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Annualized Return:** {metrics['annualized_return_pct']:.1f}%")
            st.write(f"**Sortino Ratio:** {metrics['sortino_ratio']:.2f}")
            st.write(f"**Win Rate:** {metrics['win_rate_pct']:.1f}%")
        with col2:
            st.write(f"**Average Win:** {metrics.get('avg_win_pct', 0):.1f}%")
            st.write(f"**Average Loss:** {metrics.get('avg_loss_pct', 0):.1f}%")
            st.write(f"**Profit Factor:** {metrics.get('profit_factor', 0):.2f}")
    
    # Charts
    st.markdown("---")
    
    # Portfolio Value Chart
    st.subheader("📈 Portfolio Performance")
    
    portfolio = result['portfolio']
    
    # Create portfolio value chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=portfolio.index,
        y=portfolio['total_value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#00ff88', width=2)
    ))
    
    fig.update_layout(
        title="Portfolio Value Over Time",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        template="plotly_dark",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Returns Distribution
    st.subheader("📊 Returns Distribution")
    
    returns = portfolio['daily_return'].dropna()
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=50,
        name='Daily Returns',
        marker_color='#00ff88',
        opacity=0.7
    ))
    
    fig.update_layout(
        title="Daily Returns Distribution",
        xaxis_title="Daily Return",
        yaxis_title="Frequency",
        template="plotly_dark",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent Trades
    st.subheader("💼 Recent Trades")
    
    trades = result['trades']
    if trades:
        # Convert trades to DataFrame for display
        trades_df = pd.DataFrame(trades)
        if not trades_df.empty:
            trades_df = trades_df.tail(10)  # Show last 10 trades
            st.dataframe(trades_df, use_container_width=True)
    else:
        st.info("No trades executed in this backtest.")
    
    # Download Results
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Portfolio Data"):
            csv = portfolio.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"portfolio_{selected_backtest_id}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Download Trades Data"):
            if trades:
                trades_df = pd.DataFrame(trades)
                csv = trades_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"trades_{selected_backtest_id}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No trades data to download.")

if __name__ == "__main__":
    main()