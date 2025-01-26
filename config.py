# config.py
from jesse.enums import exchanges, timeframes

# Configuration for your strategy
config = {
    'starting_balance': 10000,
    'fee': 0.001,  # 0.1% fee
    'exchange': exchanges.BINANCE,
    'symbol': 'BTC-USDT',
    'timeframe': timeframes.MINUTE_15,
}
