import ccxt
import pandas as pd

# Initialize the Binance exchange
exchange = ccxt.binance()

# Define the symbol and timeframe
symbol = 'BTC/USDT'
timeframe = '15m'

# Define the start and end dates
start_date = '2024-10-01 00:00:00'
end_date = '2024-10-03 00:00:00'

# Convert dates to timestamps
start_timestamp = exchange.parse8601(start_date)
end_timestamp = exchange.parse8601(end_date)

# Fetch historical data
candles = []
while start_timestamp < end_timestamp:
    print(f"Fetching candles starting from {exchange.iso8601(start_timestamp)}")
    new_candles = exchange.fetch_ohlcv(symbol, timeframe, since=start_timestamp)
    if not new_candles:
        break
    candles += new_candles
    start_timestamp = new_candles[-1][0] + 1  # Move to the next candle

# Convert the data to a pandas DataFrame
df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Save the data to a CSV file
df.to_csv('BTC-USDT-15m.csv', index=False)

print("Data saved to BTC-USDT-15m.csv")
