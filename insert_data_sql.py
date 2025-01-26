import sqlite3
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('BTC-USDT-15m.csv')

# Connect to the SQLite database
conn = sqlite3.connect('jesse_db.sqlite')
cursor = conn.cursor()

# Insert the data
for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO candles (exchange, symbol, timeframe, timestamp, open, close, high, low, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('binance', 'BTC-USDT', '15m', row['timestamp'], row['open'], row['close'], row['high'], row['low'], row['volume']))

# Commit the changes and close the connection
conn.commit()
conn.close()
