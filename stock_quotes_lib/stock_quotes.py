"""
Stock Quotes Module

This module provides functions to fetch and analyze stock quotes from Alpha Vantage.
"""

import os
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AlphaVantageClient:
    """Client for interacting with Alpha Vantage API."""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Alpha Vantage client.
        
        Args:
            api_key: Alpha Vantage API key. If not provided, will look for ALPHA_VANTAGE_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Alpha Vantage API key is required. Either pass it directly or set the ALPHA_VANTAGE_API_KEY environment variable."
            )
        
        # Cache to store fetched data and reduce API calls
        self._cache: Dict[str, pd.DataFrame] = {}
    
    def get_daily_time_series(self, symbol: str, outputsize: str = "compact") -> pd.DataFrame:
        """
        Fetch daily time series data for a given symbol.
        
        Args:
            symbol: The stock symbol to fetch data for.
            outputsize: Data size to retrieve. 'compact' returns the latest 100 data points,
                       'full' returns 20+ years of historical data.
            
        Returns:
            DataFrame containing the time series data.
        """
        # Check cache first
        cache_key = f"{symbol.upper()}_daily_{outputsize}"
        if cache_key in self._cache:
            logger.info(f"Using cached data for {symbol}")
            return self._cache[cache_key]
        
        # Prepare request parameters
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,  # 'compact' or 'full'
            "datatype": "json",        # Using JSON format for easier parsing
            "apikey": self.api_key,
        }
        
        # Make the request
        logger.info(f"Fetching daily time series data for {symbol} with outputsize={outputsize}")
        response = requests.get(self.BASE_URL, params=params)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
        data = response.json()
        
        # Check for error messages
        if "Error Message" in data:
            raise Exception(f"API returned an error: {data['Error Message']}")
        
        if "Time Series (Daily)" not in data:
            raise Exception(f"Unexpected API response format: {data}")
        
        # Convert to DataFrame
        time_series = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(time_series, orient="index")
        
        # Rename columns to more user-friendly names
        df.rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        }, inplace=True)
        
        # Convert string values to appropriate types
        for col in ["open", "high", "low", "close"]:
            df[col] = pd.to_numeric(df[col])
        df["volume"] = pd.to_numeric(df["volume"], downcast="integer")
        
        # Sort by date (newest first)
        df.index = pd.to_datetime(df.index)
        df.sort_index(ascending=False, inplace=True)
        
        # Store in cache
        self._cache[cache_key] = df
        
        return df


# Module-level client instance
_client: Optional[AlphaVantageClient] = None
_client_api_key: Optional[str] = None

def _get_client(api_key: Optional[str] = None) -> AlphaVantageClient:
    """
    Get or create the Alpha Vantage client instance.
    
    Args:
        api_key: Optional API key to use.
        
    Returns:
        AlphaVantageClient instance.
    """
    global _client, _client_api_key
    
    # If api_key has changed or client doesn't exist, create a new one
    if _client is None or (api_key is not None and api_key != _client_api_key):
        _client = AlphaVantageClient(api_key)
        _client_api_key = api_key
    
    return _client


def lookup(symbol: str, date: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Look up stock data for a specific symbol and date.
    
    Args:
        symbol: Stock symbol to look up.
        date: Date to look up in format 'YYYY-MM-DD'.
        api_key: Optional API key to use.
        
    Returns:
        Dictionary with stock data.
        
    Raises:
        ValueError: If the symbol or date is invalid.
    """
    client = _get_client(api_key)
    
    # Convert date string to datetime
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date_str = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date}. Use YYYY-MM-DD.")
    
    # First try with compact data (most recent 100 data points)
    outputsize = "compact"
    df = client.get_daily_time_series(symbol, outputsize=outputsize)
    
    # Convert index to string format for comparison
    df_dates = df.index.strftime('%Y-%m-%d').tolist()
    
    # If the date is not in the compact data, try with full data
    if date_str not in df_dates:
        logging.getLogger(__name__).info(f"Date {date_str} not found in compact data, trying full dataset")
        outputsize = "full"
        df = client.get_daily_time_series(symbol, outputsize=outputsize)
        df_dates = df.index.strftime('%Y-%m-%d').tolist()
    
    # Check if the date exists in the data
    if date_str not in df_dates:
        raise ValueError(f"No data available for {symbol} on {date_str}")
    
    # Get the data for the requested date
    date_idx = df.index[df_dates.index(date_str)]
    date_data = df.loc[date_idx]
    
    # Return the data as a dictionary
    return {
        "symbol": symbol,
        "date": date_str,
        "open": float(date_data["open"].iloc[0]) if hasattr(date_data["open"], "iloc") else float(date_data["open"]),
        "high": float(date_data["high"].iloc[0]) if hasattr(date_data["high"], "iloc") else float(date_data["high"]),
        "low": float(date_data["low"].iloc[0]) if hasattr(date_data["low"], "iloc") else float(date_data["low"]),
        "close": float(date_data["close"].iloc[0]) if hasattr(date_data["close"], "iloc") else float(date_data["close"]),
        "volume": int(date_data["volume"].iloc[0]) if hasattr(date_data["volume"], "iloc") else int(date_data["volume"])
    }


def get_min(symbol: str, n: int, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the minimum (lowest) price for a symbol over the last n data points.
    
    Args:
        symbol: The stock symbol to look up. For international stocks, use the appropriate suffix
               (e.g., 'TSCO.LON' for London Stock Exchange, 'SHOP.TRT' for Toronto Stock Exchange).
        n: The number of data points to consider.
        api_key: Optional Alpha Vantage API key.
        
    Returns:
        Dictionary containing the minimum price and the date it occurred.
    """
    client = _get_client(api_key)
    
    # Determine appropriate outputsize based on n
    outputsize = "compact" if n <= 100 else "full"
    
    # Fetch the time series data
    df = client.get_daily_time_series(symbol, outputsize=outputsize)
    
    # Get the last n data points
    df_subset = df.head(n)
    
    # Find the minimum low price
    min_low = df_subset["low"].min()
    min_date = df_subset["low"].idxmin().strftime("%Y-%m-%d")
    
    return {
        "symbol": symbol.upper(),
        "min_price": float(min_low),
        "date": min_date,
        "period": f"last {n} trading days"
    }


def get_max(symbol: str, n: int, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the maximum (highest) price for a symbol over the last n data points.
    
    Args:
        symbol: The stock symbol to look up. For international stocks, use the appropriate suffix
               (e.g., 'TSCO.LON' for London Stock Exchange, 'SHOP.TRT' for Toronto Stock Exchange).
        n: The number of data points to consider.
        api_key: Optional Alpha Vantage API key.
        
    Returns:
        Dictionary containing the maximum price and the date it occurred.
    """
    client = _get_client(api_key)
    
    # Determine appropriate outputsize based on n
    outputsize = "compact" if n <= 100 else "full"
    
    # Fetch the time series data
    df = client.get_daily_time_series(symbol, outputsize=outputsize)
    
    # Get the last n data points
    df_subset = df.head(n)
    
    # Find the maximum high price
    max_high = df_subset["high"].max()
    max_date = df_subset["high"].idxmax().strftime("%Y-%m-%d")
    
    return {
        "symbol": symbol.upper(),
        "max_price": float(max_high),
        "date": max_date,
        "period": f"last {n} trading days"
    }
