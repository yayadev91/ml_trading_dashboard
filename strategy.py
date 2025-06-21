import yfinance as yf
import pandas as pd
import ta
import joblib

# Load static model
model = joblib.load("xgb_model.pkl")

def fetch_data(ticker="AAPL"):
    df = yf.download(ticker, interval="5m", start="2025-05-20", end="2025-06-20")
    df.dropna(inplace=True)
    close = df['Close'].squeeze()

    df['rsi'] = ta.momentum.RSIIndicator(close=close).rsi()
    df['macd'] = ta.trend.MACD(close=close).macd_diff()
    df['ema_12'] = ta.trend.EMAIndicator(close=close, window=12).ema_indicator()
    df['ema_26'] = ta.trend.EMAIndicator(close=close, window=26).ema_indicator()
    df['volatility'] = ta.volatility.AverageTrueRange(high=df.iloc[:,1], low=df.iloc[:,2], close=close).average_true_range()
    df['return'] = close.pct_change()

    for col in ['rsi', 'macd', 'ema_12', 'ema_26', 'volatility']:
        df[f'{col}_lag1'] = df[col].shift(1)

    df.dropna(inplace=True)
    return df

def make_prediction(df):
    last_row = df.iloc[-1:]
    X = last_row[['rsi_lag1', 'macd_lag1', 'ema_12_lag1', 'ema_26_lag1', 'volatility_lag1', 'Volume', 'Close', 'return']]
    proba = model.predict_proba(X)[0, 1]
    return proba
