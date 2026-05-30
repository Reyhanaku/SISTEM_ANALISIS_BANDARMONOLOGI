import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data(ttl=300)
def get_historical_data(emiten, period="3mo"):
    try:
        ticker = yf.Ticker(f"{emiten}.JK")
        df = ticker.history(period=period)
        if not df.empty:
            df.reset_index(inplace=True)
            return df
    except:
        return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data(ttl=60)
def get_live_price(emiten):
    try:
        ticker = yf.Ticker(f"{emiten}.JK")
        df = ticker.history(period="1d")
        if not df.empty:
            return float(df['Close'].iloc[-1])
    except:
        return 0.0
    return 0.0