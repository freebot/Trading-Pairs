
---

# Trading-Pairs Strategy

This repository contains a **pairs trading strategy** implemented using Jesse, a Python framework for algorithmic trading. The strategy identifies correlated assets (e.g., `BTC-USDT` and `ETH-USDT`) and trades them when their prices diverge, expecting them to converge again.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Create SQLite Database](#create-sqlite-database)
4. [Inject Data into SQLite](#inject-data-into-sqlite)
5. [Run the Strategy](#run-the-strategy)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Jesse**: Install using `pip install jesse`
- **SQLite3**: Pre-installed on most systems. Verify with `sqlite3 --version`.
- **Git**: To clone the repository.

---

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/freebot/Trading-Pairs.git
   cd Trading-Pairs
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**:
   Create a `.env` file in the root directory with the following content:
   ```plaintext
   DB_USERNAME=
   DB_PASSWORD=
   DB_NAME=jesse_db
   DB_HOST=localhost
   DB_PORT=5432
   DB_DRIVER=sqlite
   ```

4. **Set Up the Jesse Project**:
   Ensure your directory structure looks like this:
   ```
   Trading-Pairs/
   ├── config.py
   ├── routes.py
   ├── storage/
   ├── .env
   ├── strategies/
   │   └── PairsTrading.py
   └── ...
   ```

---

## Create SQLite Database

1. **Create the Database**:
   Run the following command to create a SQLite database:
   ```bash
   sqlite3 jesse_db.sqlite
   ```

2. **Create the `candles` Table**:
   Inside the SQLite shell, create the `candles` table:
   ```sql
   CREATE TABLE candles (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       exchange TEXT NOT NULL,
       symbol TEXT NOT NULL,
       timeframe TEXT NOT NULL,
       timestamp BIGINT NOT NULL,
       open REAL NOT NULL,
       close REAL NOT NULL,
       high REAL NOT NULL,
       low REAL NOT NULL,
       volume REAL NOT NULL
   );
   ```

3. **Exit the SQLite Shell**:
   Type `.quit` or `.exit` to exit the SQLite shell.

---

## Inject Data into SQLite

1. **Fetch Historical Data**:
   Use the `ccxt` library to fetch historical data for the trading pairs. For example:
   ```python
   import ccxt
   import pandas as pd

   exchange = ccxt.binance()
   symbol = 'BTC/USDT'
   timeframe = '1h'
   start_date = '2024-10-01 00:00:00'
   end_date = '2024-10-03 00:00:00'

   start_timestamp = exchange.parse8601(start_date)
   end_timestamp = exchange.parse8601(end_date)

   candles = []
   while start_timestamp < end_timestamp:
       print(f"Fetching candles starting from {exchange.iso8601(start_timestamp)}")
       new_candles = exchange.fetch_ohlcv(symbol, timeframe, since=start_timestamp)
       if not new_candles:
           break
       candles += new_candles
       start_timestamp = new_candles[-1][0] + 1

   df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
   df.to_csv('BTC-USDT-1h.csv', index=False)
   ```

2. **Inject Data into SQLite**:
   Use the following Python script to inject the data into the SQLite database:
   ```python
   import sqlite3
   import pandas as pd

   # Load the CSV file into a DataFrame
   df = pd.read_csv('BTC-USDT-1h.csv')

   # Connect to the SQLite database
   conn = sqlite3.connect('jesse_db.sqlite')
   cursor = conn.cursor()

   # Insert the data
   for index, row in df.iterrows():
       cursor.execute('''
           INSERT INTO candles (exchange, symbol, timeframe, timestamp, open, close, high, low, volume)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
       ''', ('binance', 'BTC-USDT', '1h', row['timestamp'], row['open'], row['close'], row['high'], row['low'], row['volume']))

   # Commit the changes and close the connection
   conn.commit()
   conn.close()
   ```

---

## Run the Strategy

1. **Update `routes.py`**:
   Define the trading pairs and strategy in `routes.py`:
   ```python
   from jesse.enums import exchanges, timeframes

   routes = [
       {
           'exchange': exchanges.BINANCE,
           'symbol': 'BTC-USDT',
           'timeframe': timeframes.HOUR_1,
           'strategy': 'PairsTrading',
       },
       {
           'exchange': exchanges.BINANCE,
           'symbol': 'ETH-USDT',
           'timeframe': timeframes.HOUR_1,
           'strategy': 'PairsTrading',
       }
   ]
   ```

2. **Run the Backtest**:
   Execute the backtest using Jesse:
   ```bash
   jesse backtest
   ```

3. **Analyze the Results**:
   Use the `jesse analyze` command to visualize the results:
   ```bash
   jesse analyze
   ```

---

## Troubleshooting

- **`.env` File Not Found**:
  Ensure the `.env` file exists in the root directory and contains the correct database configuration.

- **SQLite Syntax Errors**:
  Verify the SQL queries and table schema. Test queries in the SQLite shell.

- **Data Injection Issues**:
  Ensure the CSV file is correctly formatted and the `candles` table exists.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Let me know if you need further assistance! 😊
