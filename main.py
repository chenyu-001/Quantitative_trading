import pandas as pd
import yfinance as yf
import numpy as np


def get_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data


def moving_average_crossover(data, short_window, long_window):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()

    return signals


if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2021-12-31"

    short_window = 40
    long_window = 100

    data = get_data(ticker, start_date, end_date)
    signals = moving_average_crossover(data, short_window, long_window)

    print(signals[signals.positions != 0.0])
