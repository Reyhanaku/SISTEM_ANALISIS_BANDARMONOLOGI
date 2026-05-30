import plotly.graph_objects as go
import streamlit as st

def render_candlestick(df, emiten):
    if df.empty:
        st.warning(f"Data grafik untuk {emiten} tidak tersedia.")
        return
        
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=emiten)])
                
    fig.update_layout(
        title=f"Grafik Pergerakan Harga {emiten} (3 Bulan Terakhir)",
        yaxis_title='Harga (IDR)',
        xaxis_rangeslider_visible=False,
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)