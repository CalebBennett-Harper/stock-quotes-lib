# Stock Quotes Library

A Python library for fetching stock quotes from Alpha Vantage API and performing simple operations on the data.

## Features

- Fetch daily stock data from Alpha Vantage
- Look up stock data for a specific date
- Find minimum price over a range of data points
- Find maximum price over a range of data points
- Caching to minimize API calls

## Installation

### From Source

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stock_quotes_lib.git
   cd stock_quotes_lib
   ```

2. Install the package:
   ```
   pip install -e .
   ```

### Using pip (once published)

```
pip install stock_quotes_lib
```

## Usage

### Setting up your API Key

You need an Alpha Vantage API key to use this library. You can get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

You can provide your API key in two ways:

1. Set it as an environment variable:
   ```
   export ALPHA_VANTAGE_API_KEY="your_api_key"
   ```

2. Pass it directly to the functions:
   ```python
   result = lookup("AAPL", "2023-01-10", api_key="your_api_key")
   ```

### Example Usage

```python
from stock_quotes_lib import lookup, get_min, get_max
import os

# Set your API key as an environment variable
os.environ["ALPHA_VANTAGE_API_KEY"] = "your_api_key"

# Look up stock data for a specific date
apple_data = lookup("AAPL", "2023-01-10")
print(f"Apple stock data for {apple_data['date']}:")
print(f"Open: ${apple_data['open']}")
print(f"High: ${apple_data['high']}")
print(f"Low: ${apple_data['low']}")
print(f"Close: ${apple_data['close']}")
print(f"Volume: {apple_data['volume']}")

# Find the minimum price over the last 30 data points
min_price = get_min("MSFT", 30)
print(f"\nMinimum price for Microsoft over the last 30 trading days:")
print(f"${min_price['min_price']} on {min_price['date']}")

# Find the maximum price over the last 90 data points
max_price = get_max("GOOGL", 90)
print(f"\nMaximum price for Google over the last 90 trading days:")
print(f"${max_price['max_price']} on {max_price['date']}")
```

## API Reference

### lookup(symbol, date, api_key=None)

Look up stock data for a specific symbol and date.

- `symbol`: The stock symbol to look up (e.g., "AAPL")
- `date`: The date to look up data for. Can be a string in 'YYYY-MM-DD' format or a datetime object.
- `api_key`: Optional Alpha Vantage API key.

Returns a dictionary containing:
- `symbol`: The stock symbol
- `date`: The date of the data
- `open`: The opening price
- `high`: The highest price
- `low`: The lowest price
- `close`: The closing price
- `volume`: The trading volume

### get_min(symbol, n, api_key=None)

Get the minimum (lowest) price for a symbol over the last n data points.

- `symbol`: The stock symbol to look up
- `n`: The number of data points to consider
- `api_key`: Optional Alpha Vantage API key

Returns a dictionary containing:
- `symbol`: The stock symbol
- `min_price`: The minimum price
- `date`: The date the minimum price occurred
- `period`: Description of the period considered

### get_max(symbol, n, api_key=None)

Get the maximum (highest) price for a symbol over the last n data points.

- `symbol`: The stock symbol to look up
- `n`: The number of data points to consider
- `api_key`: Optional Alpha Vantage API key

Returns a dictionary containing:
- `symbol`: The stock symbol
- `max_price`: The maximum price
- `date`: The date the maximum price occurred
- `period`: Description of the period considered

## License

MIT
