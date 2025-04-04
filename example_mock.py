"""
Example usage of the stock_quotes_lib library with mock data.
This allows you to test the library's functionality without making actual API calls.
"""

import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from stock_quotes_lib.stock_quotes import AlphaVantageClient

class MockAlphaVantageClient(AlphaVantageClient):
    """Mock client that returns predefined data instead of making API calls."""
    
    def __init__(self, api_key=None):
        # No need to validate API key for mock
        self.api_key = api_key or "mock_key"
        self._cache = {}
    
    def get_daily_time_series(self, symbol, outputsize="compact"):
        """Return mock data instead of making an API call."""
        print(f"Using mock data for {symbol} (outputsize={outputsize})")
        
        # Define special data points for specific symbols and dates
        special_data = {
            "AAPL": {
                "2025-03-28": {"open": 221.67, "high": 223.81, "low": 217.68, "close": 217.90, "volume": 39818617},
                "2020-03-20": {"open": 247.18, "high": 251.83, "low": 228.00, "close": 229.24, "volume": 100423346}
            },
            "MSFT": {
                "2025-03-28": {"open": 415.23, "high": 418.76, "low": 412.55, "close": 417.88, "volume": 22456789}
            },
            "GOOGL": {
                "2025-03-28": {"open": 190.45, "high": 195.67, "low": 189.23, "close": 193.78, "volume": 15678901},
                "2025-02-04": {"open": 205.34, "high": 207.05, "low": 203.45, "close": 206.78, "volume": 14567890}
            },
            "TSCO.LON": {
                "2025-03-28": {"open": 329.10, "high": 335.40, "low": 328.70, "close": 332.30, "volume": 26757570}
            }
        }
        
        # Start with a base date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=150)
        date_range = pd.date_range(start=start_date, end=end_date, freq='B')
        
        # Create a DataFrame with the date range as index
        df = pd.DataFrame(index=date_range)
        
        # Add mock data columns
        df['open'] = np.random.uniform(90, 110, size=len(df))
        df['high'] = df['open'] * np.random.uniform(1.0, 1.05, size=len(df))
        df['low'] = df['open'] * np.random.uniform(0.95, 1.0, size=len(df))
        df['close'] = np.random.uniform(df['low'], df['high'])
        df['volume'] = np.random.randint(500000, 5000000, size=len(df))
        
        # Add special dates to the DataFrame if they're not already in the index
        if symbol in special_data:
            for date_str, values in special_data[symbol].items():
                date_obj = pd.to_datetime(date_str)
                
                # Add the row if it doesn't exist
                if date_obj not in df.index:
                    new_row = pd.DataFrame(values, index=[date_obj])
                    df = pd.concat([df, new_row])
                else:
                    # Update existing row
                    for col, val in values.items():
                        df.at[date_obj, col] = val
        
        # Sort by date (newest first)
        df = df.sort_index(ascending=False)
        
        # If outputsize is "full", make sure we include historical dates
        if outputsize == "full" and symbol in special_data:
            for date_str in special_data[symbol]:
                date_obj = pd.to_datetime(date_str)
                if date_obj < start_date:
                    # This is a historical date outside our normal range
                    values = special_data[symbol][date_str]
                    new_row = pd.DataFrame(values, index=[date_obj])
                    df = pd.concat([df, new_row])
        
        # Final sort to make sure everything is in order
        df = df.sort_index(ascending=False)
        
        return df

# Replace the real client with our mock client
import stock_quotes_lib.stock_quotes
stock_quotes_lib.stock_quotes.AlphaVantageClient = MockAlphaVantageClient

# Now import the functions which will use our mock client
from stock_quotes_lib import lookup, get_min, get_max

def main():
    print("Stock Quotes Library Example (MOCK DATA)")
    print("========================================")
    
    # Example 1: Look up stock data for a specific date
    try:
        trading_date = "2025-03-28"
        print(f"\nLooking up Apple stock data for {trading_date}...")
        apple_data = lookup("AAPL", trading_date)
        print(f"Apple stock data for {apple_data['date']}:")
        print(f"  Open:   ${apple_data['open']:.2f}")
        print(f"  High:   ${apple_data['high']:.2f}")
        print(f"  Low:    ${apple_data['low']:.2f}")
        print(f"  Close:  ${apple_data['close']:.2f}")
        print(f"  Volume: {apple_data['volume']:,}")
    except Exception as e:
        print(f"Error looking up Apple stock: {e}")
    
    # Example 2: Find the minimum price over the last 30 data points
    try:
        print("\nFinding minimum price for Microsoft over the last 30 trading days...")
        min_price = get_min("MSFT", 30)
        print(f"Minimum price for Microsoft over the last 30 trading days:")
        print(f"  ${min_price['min_price']:.2f} on {min_price['date']}")
    except Exception as e:
        print(f"Error finding minimum price for Microsoft: {e}")
    
    # Example 3: Find the maximum price over the last 90 data points
    try:
        print("\nFinding maximum price for Google over the last 90 trading days...")
        max_price = get_max("GOOGL", 90)
        print(f"Maximum price for Google over the last 90 trading days:")
        print(f"  ${max_price['max_price']:.2f} on {max_price['date']}")
    except Exception as e:
        print(f"Error finding maximum price for Google: {e}")
    
    # Example 4: Look up international stock (London Stock Exchange)
    try:
        print(f"\nLooking up Tesco (UK) stock data for {trading_date}...")
        tesco_data = lookup("TSCO.LON", trading_date)
        print(f"Tesco stock data for {tesco_data['date']}:")
        print(f"  Open:   £{tesco_data['open']:.2f}")
        print(f"  High:   £{tesco_data['high']:.2f}")
        print(f"  Low:    £{tesco_data['low']:.2f}")
        print(f"  Close:  £{tesco_data['close']:.2f}")
        print(f"  Volume: {tesco_data['volume']:,}")
    except Exception as e:
        print(f"Error looking up Tesco stock: {e}")
    
    # Example 5: Historical data from several years ago
    try:
        historical_date = "2020-03-20"  # Date during COVID-19 market crash
        print(f"\nLooking up historical Apple stock data for {historical_date}...")
        historical_data = lookup("AAPL", historical_date)
        print(f"Apple stock data for {historical_data['date']}:")
        print(f"  Open:   ${historical_data['open']:.2f}")
        print(f"  High:   ${historical_data['high']:.2f}")
        print(f"  Low:    ${historical_data['low']:.2f}")
        print(f"  Close:  ${historical_data['close']:.2f}")
        print(f"  Volume: {historical_data['volume']:,}")
    except Exception as e:
        print(f"Error looking up historical Apple stock: {e}")

if __name__ == "__main__":
    main()
