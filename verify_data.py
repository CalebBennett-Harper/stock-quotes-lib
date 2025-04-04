"""
Verification script for stock_quotes_lib.

This script performs basic validation checks on the data returned by the library.
"""

import os
import requests
from stock_quotes_lib import lookup, get_min, get_max
import json

# Use the same API key
API_KEY = "XGRJ6U7YQAMVWWKC"

# Test date
TEST_DATE = "2025-03-28"
TEST_SYMBOL = "AAPL"

def verify_with_direct_api_call():
    """Compare library results with direct API call to verify accuracy."""
    print("Verification Test: Comparing library results with direct API call")
    print("=" * 70)
    
    # Get data using our library
    library_data = lookup(TEST_SYMBOL, TEST_DATE, api_key=API_KEY)
    print(f"\nLibrary result for {TEST_SYMBOL} on {TEST_DATE}:")
    print(json.dumps(library_data, indent=2))
    
    # Make direct API call to Alpha Vantage
    print("\nMaking direct API call to Alpha Vantage...")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": TEST_SYMBOL,
        "apikey": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract the specific date from the direct API response
    if "Time Series (Daily)" in data and TEST_DATE in data["Time Series (Daily)"]:
        direct_data = data["Time Series (Daily)"][TEST_DATE]
        print("\nDirect API result:")
        print(json.dumps(direct_data, indent=2))
        
        # Compare values
        print("\nVerification Results:")
        print("-" * 50)
        
        # Convert API data to match our format for comparison
        api_open = float(direct_data["1. open"])
        api_high = float(direct_data["2. high"])
        api_low = float(direct_data["3. low"])
        api_close = float(direct_data["4. close"])
        api_volume = int(direct_data["5. volume"])
        
        # Check if values match
        open_match = abs(library_data["open"] - api_open) < 0.01
        high_match = abs(library_data["high"] - api_high) < 0.01
        low_match = abs(library_data["low"] - api_low) < 0.01
        close_match = abs(library_data["close"] - api_close) < 0.01
        volume_match = library_data["volume"] == api_volume
        
        print(f"Open:   {library_data['open']:.2f} vs {api_open:.2f} - {'✓' if open_match else '✗'}")
        print(f"High:   {library_data['high']:.2f} vs {api_high:.2f} - {'✓' if high_match else '✗'}")
        print(f"Low:    {library_data['low']:.2f} vs {api_low:.2f} - {'✓' if low_match else '✗'}")
        print(f"Close:  {library_data['close']:.2f} vs {api_close:.2f} - {'✓' if close_match else '✗'}")
        print(f"Volume: {library_data['volume']:,} vs {api_volume:,} - {'✓' if volume_match else '✗'}")
        
        all_match = open_match and high_match and low_match and close_match and volume_match
        print("\nOverall verification:", "PASSED ✓" if all_match else "FAILED ✗")
    else:
        print(f"Error: Could not find data for {TEST_DATE} in direct API response")

def verify_min_max_functions():
    """Verify min/max functions by comparing with manual calculation."""
    print("\n\nVerification Test: Verifying min/max functions")
    print("=" * 70)
    
    # Test parameters
    test_range = 10
    
    # Get results from our library functions
    min_result = get_min(TEST_SYMBOL, test_range, api_key=API_KEY)
    max_result = get_max(TEST_SYMBOL, test_range, api_key=API_KEY)
    
    print(f"\nLibrary min result over last {test_range} days:")
    print(json.dumps(min_result, indent=2))
    
    print(f"\nLibrary max result over last {test_range} days:")
    print(json.dumps(max_result, indent=2))
    
    # Make direct API call to verify
    print("\nVerifying with direct calculation from API data...")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": TEST_SYMBOL,
        "apikey": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Time Series (Daily)" in data:
        # Sort dates in descending order (newest first)
        time_series = data["Time Series (Daily)"]
        sorted_dates = sorted(time_series.keys(), reverse=True)
        
        # Take only the first 'test_range' dates
        recent_dates = sorted_dates[:test_range]
        
        # Find min and max manually
        min_low = float('inf')
        min_date = None
        max_high = float('-inf')
        max_date = None
        
        for date in recent_dates:
            daily_data = time_series[date]
            low = float(daily_data["3. low"])
            high = float(daily_data["2. high"])
            
            if low < min_low:
                min_low = low
                min_date = date
                
            if high > max_high:
                max_high = high
                max_date = date
        
        print("\nDirect calculation results:")
        print(f"Min low:  ${min_low:.2f} on {min_date}")
        print(f"Max high: ${max_high:.2f} on {max_date}")
        
        # Compare with library results
        print("\nVerification Results:")
        print("-" * 50)
        
        min_match = abs(min_result["min_price"] - min_low) < 0.01 and min_result["date"] == min_date
        max_match = abs(max_result["max_price"] - max_high) < 0.01 and max_result["date"] == max_date
        
        print(f"Min price: {min_result['min_price']:.2f} on {min_result['date']} vs {min_low:.2f} on {min_date} - {'✓' if min_match else '✗'}")
        print(f"Max price: {max_result['max_price']:.2f} on {max_result['date']} vs {max_high:.2f} on {max_date} - {'✓' if max_match else '✗'}")
        
        print("\nOverall min/max verification:", "PASSED ✓" if min_match and max_match else "FAILED ✗")
    else:
        print("Error: Could not retrieve time series data from API")

if __name__ == "__main__":
    verify_with_direct_api_call()
    verify_min_max_functions()
