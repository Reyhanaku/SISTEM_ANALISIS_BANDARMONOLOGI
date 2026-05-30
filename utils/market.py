import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300)
def get_live_price(emiten):
    try:
        ticker = yf.Ticker(f"{emiten}.JK")
        df = ticker.history(period="1d")
        if not df.empty:
            return float(df['Close'].iloc[-1])
    except:
        return None
    return None