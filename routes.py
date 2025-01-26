# routes.py
from jesse.enums import exchanges, timeframes

routes = [
    {
        'exchange': exchanges.BINANCE,
        'symbol': 'BTC-USDT',
        'timeframe': timeframes.MINUTE_15,
        'strategy': 'MyStrategy',  # Replace with your strategy name
    }
]
