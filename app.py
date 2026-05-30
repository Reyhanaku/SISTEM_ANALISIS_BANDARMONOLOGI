import streamlit as st
from utils.auth import render_auth
from pages.analisis import render_analisis
from pages.logbook import render_logbook

st.set_page_config(page_title="Sistem Analisis VIP", page_icon="📈", layout="wide")

st.markdown("""
<style>
/* Premium UI CSS Injection */
div[data-testid="metric-container"] {
    background-color: var(--secondary-background-color);
    padding: 15px 20px;
    border-radius: 12px;
    border: 1px solid rgba(150, 150, 150, 0.15);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}
.stButton>button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s;
}
.stButton>button:hover {
    transform: scale(1.02);
}
th {
    background-color: var(--primary-color) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

if not st.session_state['logged_in']:
    render_auth()
else:
    st.sidebar.title(f"👋 Halo, {st.session_state['username']}!")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("Navigasi Dasbor", ["📊 Analisis Bandarmologi", "🎯 Log Book & Portofolio"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", width='stretch'):
        st.session_state.clear()
        st.rerun()

    st.title("Sistem Analisis Bandarmologi IHSG")
    st.markdown("---")

    if menu == "📊 Analisis Bandarmologi":
        render_analisis()
    elif menu == "🎯 Log Book & Portofolio":
        render_logbook()