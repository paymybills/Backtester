"""
Data ingestion module responsible for loading and validating market data from different sources.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
import sqlite3

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not installed. Yahoo Finance data fetching will not be available.")

class DataIngestion:
    """Class responsible for loading and validating market data from different sources."""
    
    def __init__(self):
        """Initialize the DataIngestion class."""
        self.data = None
        self.data_source = None
    
    def load_from_csv(self, file_path: str, date_format: str = '%Y-%m-%d') -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Args:  
            file_path: Path to the CSV file
            date_format: Format of the date column
            
        Returns:
            Pandas DataFrame with market data
        """
        try:
            data = pd.read_csv(file_path)
            # Convert date columns to datetime format
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'], format=date_format)
                data.set_index('Date', inplace=True)
            
            self.data = data
            self.data_source = f"CSV: {file_path}"
            print(f"Successfully loaded data from {file_path}")
            return data
        except Exception as e:
            print(f"Error loading data from CSV: {e}")
            return None
    
    def load_from_sql(self, connection_string: str, query: str) -> pd.DataFrame:
        """
        Load data from SQL database.
        
        Args:
            connection_string: SQL connection string
            query: SQL query to execute
            
        Returns:
            Pandas DataFrame with market data
        """
        try:
            conn = sqlite3.connect(connection_string)
            data = pd.read_sql(query, conn)
            
            # Convert date columns to datetime format
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
                data.set_index('Date', inplace=True)
            
            self.data = data
            self.data_source = f"SQL: {connection_string}"
            print(f"Successfully loaded data from SQL")
            return data
        except Exception as e:
            print(f"Error loading data from SQL: {e}")
            return None
    
    def generate_sample_data(self, start_date: str, end_date: str, ticker: str = 'SAMPLE') -> pd.DataFrame:
        """
        Generate sample price data for testing purposes.
        
        Args:
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'
            ticker: Ticker symbol for the generated data
            
        Returns:
            Pandas DataFrame with sample market data
        """
        # Parse dates
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        # Generate business days
        date_range = pd.date_range(start=start, end=end, freq='B')
        
        # Generate random prices with upward trend and some volatility
        n = len(date_range)
        start_price = 100
        
        # Base trend (arithmetic Brownian motion with drift)
        trend = np.linspace(0, 30, n)  # Upward drift
        noise = np.random.normal(0, 1, n) * 2  # Daily volatility
        prices = start_price + trend + noise.cumsum()  # Cumulative noise for random walk
        
        # Ensure no negative prices
        prices = np.maximum(prices, 0.01)
        
        # Calculate OHLC from close prices with some intraday variation
        close = prices
        high = close * (1 + np.random.uniform(0, 0.015, n))
        low = close * (1 - np.random.uniform(0, 0.015, n))
        open_price = low + np.random.uniform(0, 1, n) * (high - low)
        
        # Generate volume with some correlation to price changes
        price_changes = np.diff(close, prepend=close[0])
        volume = np.abs(price_changes) * 1000000 + np.random.uniform(500000, 1500000, n)
        
        # Create DataFrame
        data = pd.DataFrame({
            'Open': open_price,
            'High': high,
            'Low': low,
            'Close': close,
            'Volume': volume.astype(int),
            'Ticker': ticker
        }, index=date_range)
        
        data.index.name = 'Date'
        self.data = data
        self.data_source = f"Generated sample data for {ticker}"
        print(f"Successfully generated sample data for {ticker}")
        return data
    
    def load_from_yahoo(self, ticker: str, start_date: str, end_date: str, interval: str = "1d") -> pd.DataFrame:
        """
        Load data from Yahoo Finance.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'
            interval: Data frequency - "1m", "5m", "15m", "1h", "1d" (default), "1wk", "1mo"
                     Note: Yahoo Finance has limitations on historical intraday data
            
        Returns:
            Pandas DataFrame with market data from Yahoo Finance
        """
        if not YFINANCE_AVAILABLE:
            raise ImportError("yfinance library is not installed. Install it with: pip install yfinance")
        
        try:
            # Ensure ticker is a string (not tuple or list)
            if isinstance(ticker, (tuple, list)):
                ticker = ticker[0] if ticker else "AAPL"
            ticker = str(ticker).strip().upper()
            
            # Ensure dates are strings
            start_date = str(start_date)
            end_date = str(end_date)
            
            print(f"Fetching data for {ticker} from Yahoo Finance ({start_date} to {end_date}, interval={interval})...")
            
            # Download data from Yahoo Finance
            data = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
            
            if data.empty:
                print(f"No data found for {ticker} in the specified date range")
                return None
            
            # Flatten multi-level columns if present (happens with single ticker)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            # Ensure we have the required columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_cols = [col for col in required_cols if col not in data.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Add ticker column
            data['Ticker'] = ticker
            
            self.data = data
            self.data_source = f"Yahoo Finance: {ticker}"
            print(f"Successfully loaded {len(data)} rows for {ticker} from Yahoo Finance")
            return data
            
        except Exception as e:
            print(f"Error loading data from Yahoo Finance: {e}")
            return None
    
    def validate_data(self) -> bool:
        """
        Validate the loaded data to ensure quality and consistency.
        
        Returns:
            Boolean indicating if data is valid
        """
        if self.data is None:
            print("No data loaded to validate")
            return False
        
        # Check for required columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")
            return False
        
        # Check for missing values
        missing_values = self.data[required_columns].isnull().sum().sum()
        if missing_values > 0:
            print(f"Warning: Found {missing_values} missing values in price data")
        
        # Check for price consistency (High ≥ Open, High ≥ Close, Low ≤ Open, Low ≤ Close)
        inconsistencies = (
            (self.data['High'] < self.data['Open']) | 
            (self.data['High'] < self.data['Close']) | 
            (self.data['Low'] > self.data['Open']) | 
            (self.data['Low'] > self.data['Close'])
        ).sum()
        
        if inconsistencies > 0:
            print(f"Warning: Found {inconsistencies} price inconsistencies")
            return False
        
        print("Data validation passed")
        return True