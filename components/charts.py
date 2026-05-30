import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_candlestick(df, emiten):
    if df.empty:
        st.warning(f"Data grafik untuk {emiten} tidak tersedia.")
        return
        
    # --- HITUNG INDIKATOR TEKNIKAL (MOVING AVERAGE) ---
    df['MA20'] = df['Close'].rolling(window=20).mean() # Tren Jangka Pendek
    df['MA50'] = df['Close'].rolling(window=50).mean() # Tren Menengah
        
    fig = go.Figure()
    
    # 1. Candlestick Utama
    fig.add_trace(go.Candlestick(x=df['Date'],
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'],
                name=emiten))
                
    # 2. Garis MA20 (Kuning) - Indikator Tren Jangka Pendek
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], 
                line=dict(color='yellow', width=1.5), 
                name='MA 20 (Tren Pendek)'))
                
    # 3. Garis MA50 (Merah) - Indikator Batas Sell/Distribusi
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], 
                line=dict(color='red', width=1.5), 
                name='MA 50 (Batas Sell)'))
                
    fig.update_layout(
        title=f"Grafik & Indikator Teknikal {emiten} (3 Bulan Terakhir)",
        yaxis_title='Harga (IDR)',
        xaxis_rangeslider_visible=False,
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
