import streamlit as st
from strategy import fetch_data, make_prediction
from portfolio import PaperPortfolio
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="📈 ML Paper Trading Bot", layout="wide")
st.title("📊 Machine Learning Paper Trading Dashboard")
# === Session state ===
if "portfolio" not in st.session_state:
    st.session_state.portfolio = PaperPortfolio()

# === Strategy logic ===
ticker = "AAPL"
df = fetch_data(ticker)
proba = make_prediction(df)
price = df.iloc["Close",-1]
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
st.write(price)
st.write(f"### 🔮 Prediction: {proba:.3f} | 📈 Price: ${price:.2f} | 🕒 {timestamp}")

# === Trading logic ===
threshold = 0.6
portfolio = st.session_state.portfolio

if proba > threshold and portfolio.position == 0:
    portfolio.buy(price, timestamp)
elif proba < (1 - threshold) and portfolio.position == 1:
    portfolio.sell(price, timestamp)

portfolio.update_equity(price)

# === Display Trade Log ===
st.subheader("🧾 Trade Log")
st.dataframe(portfolio.trade_log[::-1])

# === Equity curve ===
st.subheader("📈 Equity Curve")
st.line_chart(portfolio.equity_curve)

# === Current state ===
st.metric("💰 Cash", f"${portfolio.cash:.2f}")
st.metric("📊 Equity", f"${portfolio.current_equity():.2f}")

# === Export button
if st.button("💾 Export trades as CSV"):
    path = "trades.csv"
    portfolio.export_trades_csv(path)
    with open(path, "rb") as f:
        st.download_button("Download CSV", f, file_name="trades.csv")
