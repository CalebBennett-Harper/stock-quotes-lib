"""
Terminal usage examples for stock_quotes_lib.

This script demonstrates how to use the stock_quotes_lib directly from the terminal
without making additional API calls (using mock data).
"""

import json
from datetime import datetime, timedelta

# Mock data to demonstrate usage without making API calls
MOCK_DATA = {
    "AAPL": {
        "2025-03-28": {
            "open": 221.67,
            "high": 223.81,
            "low": 217.68,
            "close": 217.90,
            "volume": 39818617
        },
        "min_price": {
            "price": 187.34,
            "date": "2025-04-04"
        },
        "max_price": {
            "price": 225.62,
            "date": "2025-03-31"
        }
    },
    "MSFT": {
        "2025-03-28": {
            "open": 415.23,
            "high": 418.76,
            "low": 412.55,
            "close": 417.88,
            "volume": 22456789
        },
        "min_price": {
            "price": 359.49,
            "date": "2025-04-04"
        },
        "max_price": {
            "price": 419.25,
            "date": "2025-03-25"
        }
    }
}

def demo_terminal_usage():
    """
    Demonstrate how to use the library from the terminal.
    """
    print("Stock Quotes Library - Terminal Usage Examples")
    print("=============================================")
    
    print("\n1. Basic Usage (with API calls - currently rate limited)")
    print("--------------------------------------------------")
    print("# Import the library")
    print("from stock_quotes_lib import lookup, get_min, get_max")
    print("\n# Set your API key")
    print("import os")
    print("os.environ['ALPHA_VANTAGE_API_KEY'] = 'YOUR_API_KEY'")
    print("\n# Look up a stock")
    print("data = lookup('AAPL', '2025-03-28')")
    print("print(data)")
    
    print("\n2. Using the Library with Mock Data (no API calls)")
    print("--------------------------------------------------")
    print("# Example of what the data would look like:")
    apple_data = MOCK_DATA["AAPL"]["2025-03-28"]
    print(f"Apple stock data for 2025-03-28:")
    print(f"  Open:   ${apple_data['open']:.2f}")
    print(f"  High:   ${apple_data['high']:.2f}")
    print(f"  Low:    ${apple_data['low']:.2f}")
    print(f"  Close:  ${apple_data['close']:.2f}")
    print(f"  Volume: {apple_data['volume']:,}")
    
    print("\n3. Command-line One-liners")
    print("--------------------------------------------------")
    print("# Get stock data and format as JSON")
    print("python -c \"from stock_quotes_lib import lookup; import json; print(json.dumps(lookup('AAPL', '2025-03-28'), indent=2))\"")
    
    print("\n# Find minimum price in the last 30 days")
    print("python -c \"from stock_quotes_lib import get_min; print(get_min('MSFT', 30)['min_price'])\"")
    
    print("\n4. Creating a Custom Script")
    print("--------------------------------------------------")
    print("# Create a file named 'get_stock.py' with this content:")
    print("'''\n#!/usr/bin/env python")
    print("import sys")
    print("from stock_quotes_lib import lookup")
    print("\ndef main():")
    print("    if len(sys.argv) < 3:")
    print("        print('Usage: get_stock.py SYMBOL DATE')")
    print("        sys.exit(1)")
    print("    ")
    print("    symbol = sys.argv[1]")
    print("    date = sys.argv[2]")
    print("    ")
    print("    try:")
    print("        data = lookup(symbol, date)")
    print("        print(f'{symbol} on {date}:')")
    print("        print(f'  Open:   ${data[\"open\"]:.2f}')")
    print("        print(f'  High:   ${data[\"high\"]:.2f}')")
    print("        print(f'  Low:    ${data[\"low\"]:.2f}')")
    print("        print(f'  Close:  ${data[\"close\"]:.2f}')")
    print("        print(f'  Volume: {data[\"volume\"]:,}')")
    print("    except Exception as e:")
    print("        print(f'Error: {e}')")
    print("\nif __name__ == '__main__':")
    print("    main()")
    print("'''")
    print("\n# Make it executable:")
    print("chmod +x get_stock.py")
    print("\n# Run it:")
    print("./get_stock.py AAPL 2025-03-28")
    
    print("\n5. Using the Python REPL")
    print("--------------------------------------------------")
    print("# Start Python in interactive mode:")
    print("python")
    print("\n# Then type:")
    print(">>> from stock_quotes_lib import lookup, get_min, get_max")
    print(">>> lookup('AAPL', '2025-03-28')")
    print(">>> get_min('MSFT', 30)")
    print(">>> get_max('GOOGL', 90)")

if __name__ == "__main__":
    demo_terminal_usage()
