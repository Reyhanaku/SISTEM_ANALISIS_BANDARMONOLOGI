import streamlit as st
from utils.auth import render_auth

# Pastikan folder Anda bernama 'views' (rename dari 'pages')
from views import dashboard, journal, help_page # <--- TAMBAHAN: Import help_page

st.set_page_config(page_title="BandarLogi Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- CSS PREMIUM & MODERN INJECTION ---
st.markdown("""
<style>
/* Menyembunyikan menu navigasi default Streamlit yang kaku */
[data-testid="stSidebarNav"] {display: none !important;}

/* Styling Judul Utama dengan Gradasi Mewah */
.premium-title {
    background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.2rem;
    font-weight: 900;
    margin-bottom: 0px;
    letter-spacing: -1px;
}
.premium-subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
    font-weight: 400;
    margin-top: -5px;
    margin-bottom: 30px;
}

/* Profil Card di Sidebar (Glassmorphism Effect) */
.profile-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1));
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 25px;
    border: 1px solid rgba(139,92,246,0.2);
    backdrop-filter: blur(10px);
}
.profile-img {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    margin-bottom: 12px;
    border: 2px solid #8b5cf6;
    object-fit: cover;
    padding: 2px;
}

/* Metrik Card Hover Effect */
div[data-testid="metric-container"] {
    background-color: rgba(30, 41, 59, 0.4) !important;
    padding: 15px 20px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    border-color: rgba(139,92,246,0.5);
    box-shadow: 0 10px 15px rgba(139,92,246,0.1);
}

/* Tombol Elegan */
.stButton>button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    transition: all 0.2s;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
.stButton>button:hover {
    transform: scale(1.02);
    border-color: #3b82f6 !important;
    color: #3b82f6 !important;
}
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# --- ROUTER UTAMA ---
if not st.session_state['logged_in']:
    render_auth()
else:
    # --- SIDEBAR MEWAH ---
    st.sidebar.markdown(f"""
    <div class="profile-card">
        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state['username']}&backgroundColor=b6e3f4" class="profile-img">
        <h3 style="margin:0; font-weight:800; color:white;">{st.session_state['username'].upper()}</h3>
        <p style="margin:0; color:#94a3b8; font-size:13px; margin-top:4px;">💎 VIP Trader Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # <--- TAMBAHAN: Menambah "📘 Panduan Penggunaan" ke dalam Menu
    menu = st.sidebar.radio("Main Menu", ["⚡ Terminal Analisis", "🎯 Portofolio & Jurnal", "📘 Panduan Penggunaan"])
    st.sidebar.markdown("---")
    
    if st.sidebar.button("Keluar (Logout)", width='stretch'):
        st.session_state.clear()
        st.rerun()

    # --- HEADER KONTEN UTAMA ---
    st.markdown('<h1 class="premium-title">BandarLogi Terminal.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="premium-subtitle">Analisis jejak bandar, eksekusi trading plan, dan pantau portofolio Anda dalam satu layar.</p>', unsafe_allow_html=True)

    # <--- TAMBAHAN: Routing ke halaman help_page
    if menu == "⚡ Terminal Analisis":
        dashboard.render()
    elif menu == "🎯 Portofolio & Jurnal":
        journal.render()
    elif menu == "📘 Panduan Penggunaan":
        help_page.render()
