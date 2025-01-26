from jesse.strategies import Strategy
import jesse.indicators as ta
import numpy as np
import pandas as pd

class PairsTrading(Strategy):
    def should_long(self) -> bool:
        # Fetch historical data for the two assets
        _, asset1 = self.get_candles('Binance', 'BTC-USDT', '15m')
        _, asset2 = self.get_candles('Binance', 'ETH-USDT', '15m')

        # Calculate the spread
        spread = asset1[:, 2] - asset2[:, 2]  # Close prices

        # Calculate z-scores
        mean = np.mean(spread)
        std = np.std(spread)
        z_scores = (spread - mean) / std

        # Entry condition: z-score > 2 (spread is too wide)
        return z_scores[-1] > 2

    def should_short(self) -> bool:
        # Fetch historical data for the two assets
        _, asset1 = self.get_candles('Binance', 'BTC-USDT', '15m')
        _, asset2 = self.get_candles('Binance', 'ETH-USDT', '15m')

        # Calculate the spread
        spread = asset1[:, 2] - asset2[:, 2]  # Close prices

        # Calculate z-scores
        mean = np.mean(spread)
        std = np.std(spread)
        z_scores = (spread - mean) / std

        # Entry condition: z-score < -2 (spread is too narrow)
        return z_scores[-1] < -2

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        # Go long on the underperforming asset and short on the outperforming asset
        self.buy = 1, self.price  # Long BTC-USDT
        self.sell = 1, self.price  # Short ETH-USDT

    def go_short(self):
        # Go short on the underperforming asset and long on the outperforming asset
        self.sell = 1, self.price  # Short BTC-USDT
        self.buy = 1, self.price  # Long ETH-USDT
