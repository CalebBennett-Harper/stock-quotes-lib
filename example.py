"""
Example usage of the stock_quotes_lib library.
"""

import os
from stock_quotes_lib import lookup, get_min, get_max
from datetime import datetime, timedelta

# Set your Alpha Vantage API key as an environment variable
# os.environ["ALPHA_VANTAGE_API_KEY"] = "YOUR_API_KEY_HERE"

# Or use it directly (not recommended for production code)
API_KEY = "YOUR_API_KEY_HERE"  # Alpha Vantage API key

# Use a known trading day instead of calculating a recent date
# Markets are closed on weekends and holidays, so using a specific known trading day
trading_date = "2025-03-28"  # Using a recent Friday which should have trading data

def main():
    print("Stock Quotes Library Example")
    print("============================")
    
    # Example 1: Look up stock data for a specific date
    try:
        print(f"\nLooking up Apple stock data for {trading_date}...")
        apple_data = lookup("AAPL", trading_date, api_key=API_KEY)
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
        min_price = get_min("MSFT", 30, api_key=API_KEY)
        print(f"Minimum price for Microsoft over the last 30 trading days:")
        print(f"  ${min_price['min_price']:.2f} on {min_price['date']}")
    except Exception as e:
        print(f"Error finding minimum price for Microsoft: {e}")
    
    # Example 3: Find the maximum price over the last 90 data points
    try:
        print("\nFinding maximum price for Google over the last 90 trading days...")
        max_price = get_max("GOOGL", 90, api_key=API_KEY)
        print(f"Maximum price for Google over the last 90 trading days:")
        print(f"  ${max_price['max_price']:.2f} on {max_price['date']}")
    except Exception as e:
        print(f"Error finding maximum price for Google: {e}")
    
    # Example 4: Look up international stock (London Stock Exchange)
    try:
        print(f"\nLooking up Tesco (UK) stock data for {trading_date}...")
        tesco_data = lookup("TSCO.LON", trading_date, api_key=API_KEY)
        print(f"Tesco stock data for {tesco_data['date']}:")
        print(f"  Open:   £{tesco_data['open']:.2f}")
        print(f"  High:   £{tesco_data['high']:.2f}")
        print(f"  Low:    £{tesco_data['low']:.2f}")
        print(f"  Close:  £{tesco_data['close']:.2f}")
        print(f"  Volume: {tesco_data['volume']:,}")
    except Exception as e:
        print(f"Error looking up Tesco stock: {e}")
    
    # Example 5: Historical data from several years ago (using full dataset)
    try:
        historical_date = "2020-03-20"  # Date during COVID-19 market crash
        print(f"\nLooking up historical Apple stock data for {historical_date}...")
        historical_data = lookup("AAPL", historical_date, api_key=API_KEY)
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
