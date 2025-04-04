#!/usr/bin/env python
"""
Simple test script to verify the API key is working correctly.
"""

import os
import requests
from pprint import pprint

# Your new API key
API_KEY = "YOUR_API_KEY_HERE"

def test_api_key():
    """Test the API key with a direct call to Alpha Vantage."""
    print(f"Testing API key: {API_KEY}")
    
    # Make a simple request to Alpha Vantage
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "AAPL",
        "outputsize": "compact",
        "apikey": API_KEY
    }
    
    print("Making direct API request to Alpha Vantage...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    
    # Check for error messages
    if "Error Message" in data:
        print(f"API Error: {data['Error Message']}")
        return
    
    if "Information" in data:
        print(f"API Information: {data['Information']}")
        return
    
    if "Time Series (Daily)" not in data:
        print("Unexpected API response format:")
        pprint(data)
        return
    
    # Success!
    print("API key is working correctly!")
    
    # Get the most recent data point
    time_series = data["Time Series (Daily)"]
    most_recent_date = list(time_series.keys())[0]
    most_recent_data = time_series[most_recent_date]
    
    print(f"\nMost recent data for AAPL ({most_recent_date}):")
    print(f"  Open:   ${float(most_recent_data['1. open']):.2f}")
    print(f"  High:   ${float(most_recent_data['2. high']):.2f}")
    print(f"  Low:    ${float(most_recent_data['3. low']):.2f}")
    print(f"  Close:  ${float(most_recent_data['4. close']):.2f}")
    print(f"  Volume: {int(most_recent_data['5. volume']):,}")

if __name__ == "__main__":
    test_api_key()
