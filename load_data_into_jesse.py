from jesse import research
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('BTC-USDT-15m.csv')

# Convert the DataFrame to Jesse's candle format
candles = df[['timestamp', 'open', 'close', 'high', 'low', 'volume']].values

# Use the candles in Jesse
# For example, calculate the RSI using pandas-ta
import pandas_ta as ta

# Calculate RSI
df['rsi'] = ta.rsi(df['close'], length=14)

# Plot the results
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 8))

# Plot Close Price
plt.subplot(2, 1, 1)
plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
plt.title('Close Price')
plt.legend()

# Plot RSI
plt.subplot(2, 1, 2)
plt.plot(df['timestamp'], df['rsi'], label='RSI', color='orange')
plt.axhline(70, color='red', linestyle='--', label='Overbought')
plt.axhline(30, color='green', linestyle='--', label='Oversold')
plt.title('RSI')
plt.legend()

plt.tight_layout()
plt.show()
