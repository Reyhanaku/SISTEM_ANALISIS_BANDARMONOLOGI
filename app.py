import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Dasbor Trading", page_icon="💎", layout="wide")

st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: rgba(28, 131, 225, 0.1);
    border: 1px solid rgba(28, 131, 225, 0.5);
    padding: 5% 5% 5% 10%;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ==============================================================
GAS_URL = "https://script.google.com/macros/s/AKfycbztzJL_waRDfHgmfgxLZN4em1N6RikwOBAvv7Q-9csLxWCOGAbFPUh219JAmP4Tgw/exec"
# ==============================================================

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'brokers' not in st.session_state:
    st.session_state['brokers'] = []

if not st.session_state['logged_in']:
    st.title("🔐 Akses Dasbor Trading")
    tab_login, tab_register, tab_forgot = st.tabs(["🔑 Masuk", "📝 Daftar Baru", "🆘 Reset Password"])
    
    with tab_login:
        st.markdown("Selamat datang kembali! Masuk untuk amankan portofolio kamu.")
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Masuk", use_container_width=True)
            if submit_login:
                with st.spinner("Memverifikasi data..."):
                    try:
                        res = requests.post(GAS_URL, json={"action": "login", "username": username_input, "password": password_input}, allow_redirects=True)
                        data = res.json()
                        if data.get("status") == "success":
                            st.session_state['logged_in'] = True
                            st.session_state['username'] = username_input
                            st.rerun()
                        else:
                            st.error(data.get("message", "Gagal login."))
                    except:
                        st.error("Gagal terhubung.")
                            
    with tab_register:
        st.markdown("Mulai trading lebih pintar. Registrasi akun kamu di sini (100% Free).")
        with st.form("register_form"):
            new_user = st.text_input("Buat Username")
            new_email = st.text_input("Alamat Email")
            new_pass = st.text_input("Buat Password", type="password")
            conf_pass = st.text_input("Konfirmasi Password", type="password")
            if st.form_submit_button("Daftar Sekarang", use_container_width=True):
                if new_pass != conf_pass:
                    st.error("Password tidak cocok!")
                else:
                    try:
                        res = requests.post(GAS_URL, json={"action": "register", "username": new_user, "password": new_pass, "email": new_email}, allow_redirects=True)
                        st.success(res.json().get("message"))
                    except:
                        st.error("Gagal mendaftar.")
                            
    with tab_forgot:
        st.markdown("Lupa password itu wajar. Kasih tahu username kamu, biar sistem yang urus sisanya.")
        with st.form("forgot_form"):
            f_user = st.text_input("Masukkan Username Anda")
            if st.form_submit_button("Kirim Password via Email", use_container_width=True):
                try:
                    res = requests.post(GAS_URL, json={"action": "forgot_password", "username": f_user}, allow_redirects=True)
                    st.success(res.json().get("message"))
                except:
                    st.error("Gagal mengirim.")

else:
    if not st.session_state['brokers']:
        try:
            res = requests.get(GAS_URL)
            if res.status_code == 200:
                st.session_state['brokers'] = res.json().get('brokers', [])
        except:
            st.session_state['brokers'] = []
            
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("💎 Dasbor Trading Terpadu")
    with col_logout:
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()
            
    st.markdown(f"Selamat datang, **{st.session_state['username']}**.")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Input Data", "🎯 Log Book", "🏆 Jurnal", "📡 Radar Screener"])
    
    with tab1:
        st.subheader("Input Data Analisis")
        col_emiten, col_net = st.columns(2)
        with col_emiten:
            emiten = st.text_input("Kode Emiten").upper()
        with col_net:
            total_net_buy = st.number_input("Total Net Buy", min_value=0.0, format="%.2f")
            
        st.write("### Top 5 Buyers & Sellers")
        col_buy, col_sell = st.columns(2)
        with col_buy:
            b1, b2, b3, b4, b5 = [st.selectbox(f"Buyer {i}", [""] + st.session_state['brokers'], key=f"b{i}") for i in range(1, 6)]
        with col_sell:
            s1, s2, s3, s4, s5 = [st.selectbox(f"Seller {i}", [""] + st.session_state['brokers'], key=f"s{i}") for i in range(1, 6)]
            
        if st.button("🚀 Proses Data ke Sistem", use_container_width=True):
            if emiten:
                with st.spinner("Memproses data..."):
                    payload = {"action": "input_data", "emiten": emiten, "total_net_buy": total_net_buy, "by1": b1, "by2": b2, "by3": b3, "by4": b4, "by5": b5, "sl1": s1, "sl2": s2, "sl3": s3, "sl4": s4, "sl5": s5}
                    try:
                        res = requests.post(GAS_URL, json=payload, allow_redirects=True)
                        if res.status_code == 200:
                            st.session_state['hasil_analisis'] = res.json()
                            st.session_state['emiten'] = emiten
                            st.success(f"Data {emiten} berhasil diproses!")
                    except:
                        st.error("Gagal terhubung.")
                        
        if 'hasil_analisis' in st.session_state:
            res = st.session_state['hasil_analisis']
            em_code = st.session_state['emiten']
            st.markdown("---")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Scor Beli", res.get('scor_beli', 0))
            k2.metric("Scor Jual", res.get('scor_jual', 0))
            k3.metric("Status Analisis", res.get('status_spk', '-'))
            k4.metric("Grade", res.get('grade', '-'))
            
            st.write("### Trading Plan")
            t1, t2, t3, t4, t5 = st.columns(5)
            t1.metric("Entry", res.get('entry_price', 0))
            t2.metric("TP 1", res.get('tp1', 0))
            t3.metric("TP 2", res.get('tp2', 0))
            t4.metric("TP 3", res.get('tp3', 0))
            t5.metric("Cutloss", res.get('cutloss', 0))
            
            st.markdown("---")
            st.subheader(f"📈 Visualisasi Chart {em_code}")
            try:
                hist_data = yf.download(em_code + ".JK", period="3mo", progress=False)
                if not hist_data.empty:
                    fig = go.Figure(data=[go.Candlestick(x=hist_data.index,
                                    open=hist_data['Open'].squeeze(),
                                    high=hist_data['High'].squeeze(),
                                    low=hist_data['Low'].squeeze(),
                                    close=hist_data['Close'].squeeze())])
                    fig.update_layout(title=f"Pergerakan Harga {em_code} (3 Bulan Terakhir)", xaxis_title="Tanggal", yaxis_title="Harga", template="plotly_dark", margin=dict(l=0, r=0, t=40, b=0))
                    st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Gagal memuat grafik. Pastikan kode emiten valid di bursa IHSG.")
            
            st.markdown("---")
            with st.form("log_book_form"):
                col_tgl, col_lot = st.columns(2)
                with col_tgl: tanggal = st.date_input("Tanggal Pantauan", datetime.today())
                with col_lot: lot_beli = st.number_input("Jumlah Lot", min_value=1, step=1, value=10)
                
                if st.form_submit_button("Simpan ke Log Book", use_container_width=True):
                    payload = {
                        "action": "save_logbook", "username": st.session_state['username'], "emiten": em_code,
                        "entry_price": res.get('entry_price', 0), "tp1": res.get('tp1', 0), "tp2": res.get('tp2', 0),
                        "tp3": res.get('tp3', 0), "cutloss": res.get('cutloss', 0), "grade": res.get('grade', '-'),
                        "tanggal": tanggal.strftime("%Y-%m-%d"), "lot": lot_beli
                    }
                    try:
                        if requests.post(GAS_URL, json=payload, allow_redirects=True).status_code == 200:
                            st.success("Tersimpan di Log Book!")
                    except:
                        st.error("Gagal menyimpan.")

    with tab2:
        c_title, c_btn = st.columns([3, 1])
        with c_title:
            st.subheader("Pantauan Portofolio Aktif")
        with c_btn:
            refresh = st.button("🔄 Refresh Harga Real-Time", use_container_width=True)
            
        if refresh or 'logbook_data' not in st.session_state:
            with st.spinner("Mengambil harga instan dari market..."):
                try:
                    log_res = requests.post(GAS_URL, json={"action": "get_logbook", "username": st.session_state['username']}, allow_redirects=True)
                    if log_res.status_code == 200:
                        raw_data = log_res.json().get("data", [])
                        if raw_data:
                            emiten_list = [d["Emiten"] + ".JK" for d in raw_data]
                            market_data = yf.download(emiten_list, period="1d", group_by="ticker", threads=True, progress=False)
                            for row in raw_data:
                                em_code = row["Emiten"] + ".JK"
                                try:
                                    if len(emiten_list) == 1:
                                        live_price = float(market_data['Close'].iloc[-1])
                                    else:
                                        live_price = float(market_data[em_code]['Close'].iloc[-1])
                                except:
                                    live_price = float(row["Live Price"] if row["Live Price"] else 0)
                                
                                row["Live Price"] = live_price
                                entry = float(row["Entry Price"])
                                lot = float(row["Lot"])
                                tp1 = float(row["TP 1"])
                                tp3 = float(row["TP 3"])
                                cl = float(row["Cutloss Price"])
                                
                                pnl_rp = (live_price - entry) * lot * 100
                                row["Profit (Rp)"] = f"Rp {pnl_rp:,.0f}"
                                row["Persentase"] = f"{((live_price - entry) / entry * 100):.2f}%" if entry > 0 else "0%"
                                
                                if live_price >= tp3: row["Status"] = "🚀 TP 3 HIT!"
                                elif live_price >= float(row["TP 2"]): row["Status"] = "🔥 TP 2 HIT!"
                                elif live_price >= tp1: row["Status"] = "🛡️ RISK-FREE"
                                elif live_price <= cl: row["Status"] = "🚨 CUTLOSS!"
                                else: row["Status"] = "⏳ HOLD"
                        st.session_state['logbook_data'] = raw_data
                except:
                    st.error("Kesalahan jaringan.")
                    
        if 'logbook_data' in st.session_state:
            df_logbook = pd.DataFrame(st.session_state['logbook_data'])
            if not df_logbook.empty:
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("📌 Saham Dipantau", len(df_logbook))
                m2.metric("⏳ HOLD / RISK-FREE", len(df_logbook[df_logbook['Status'].str.contains("HOLD|RISK", case=False, na=False)]))
                m3.metric("🚀 Kena TP", len(df_logbook[df_logbook['Status'].str.contains("TP", case=False, na=False)]))
                m4.metric("🚨 Kena Cutloss", len(df_logbook[df_logbook['Status'].str.contains("CUTLOSS", case=False, na=False)]))
                
                st.markdown("---")
                def style_df(df):
                    def highlight(val):
                        v = str(val).upper()
                        if 'TP' in v: return 'background-color: rgba(39, 174, 96, 0.2); color: #2ecc71; font-weight:bold;'
                        if 'CUTLOSS' in v or '-' in v: return 'color: #e74c3c; font-weight:bold;'
                        if 'RISK' in v: return 'background-color: rgba(41, 128, 185, 0.2); color: #3498db; font-weight:bold;'
                        if 'HOLD' in v: return 'color: #f39c12; font-weight:bold;'
                        if v.replace('.','',1).replace('%','').isdigit() and float(v.replace('%','')) > 0: return 'color: #2ecc71; font-weight:bold;'
                        return ''
                    try: return df.style.map(highlight, subset=['Status', 'Persentase', 'Profit (Rp)'])
                    except: return df.style.applymap(highlight, subset=['Status', 'Persentase', 'Profit (Rp)'])
                        
                st.dataframe(style_df(df_logbook), use_container_width=True, hide_index=True)
                st.markdown("---")
                
                emiten_list = df_logbook['Emiten'].tolist()
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("#### ✏️ Edit (Avg Up/Down)")
                    edit_em = st.selectbox("Pilih Saham", emiten_list, key="ed")
                    with st.expander("Buka Form Edit"):
                        if edit_em:
                            curr_data = df_logbook[df_logbook['Emiten'] == edit_em].iloc[0]
                            new_entry = st.number_input("Avg Entry Baru", value=float(curr_data['Entry Price']))
                            new_lot = st.number_input("Lot Baru", value=int(curr_data['Lot']), step=1)
                            new_tp1 = st.number_input("TP 1 Baru", value=float(curr_data['TP 1']))
                            new_tp2 = st.number_input("TP 2 Baru", value=float(curr_data['TP 2']))
                            new_tp3 = st.number_input("TP 3 Baru", value=float(curr_data['TP 3']))
                            new_cl = st.number_input("Cutloss Baru", value=float(curr_data['Cutloss Price']))
                            if st.button("Update Data", use_container_width=True):
                                with st.spinner("Menyimpan..."):
                                    payload = {"action": "update_logbook", "username": st.session_state['username'], "emiten": edit_em, "entry_price": new_entry, "lot": new_lot, "tp1": new_tp1, "tp2": new_tp2, "tp3": new_tp3, "cutloss": new_cl}
                                    requests.post(GAS_URL, json=payload)
                                    st.session_state.pop('logbook_data', None)
                                    st.rerun()

                with c2:
                    st.markdown("#### 🏆 Selesai Trading")
                    move_em = st.selectbox("Arsipkan ke Jurnal", emiten_list, key="mv")
                    if st.button("Pindah ke Jurnal", use_container_width=True, type='primary'):
                        with st.spinner("Memindahkan..."):
                            requests.post(GAS_URL, json={"action": "move_to_history", "username": st.session_state['username'], "emiten": move_em})
                            st.session_state.pop('logbook_data', None)
                            st.session_state.pop('history_data', None)
                            st.rerun()

                with c3:
                    st.markdown("#### 🗑 Hapus Data")
                    del_em = st.selectbox("Hapus Permanen", emiten_list, key="dl")
                    if st.button("Hapus Emiten", use_container_width=True):
                        with st.spinner("Menghapus..."):
                            requests.post(GAS_URL, json={"action": "delete_logbook", "username": st.session_state['username'], "emiten": del_em})
                            st.session_state.pop('logbook_data', None)
                            st.rerun()
            else:
                st.info("📂 Log Book Anda masih kosong.")

    with tab3:
        c_ht, c_hb = st.columns([3, 1])
        with c_ht:
            st.subheader("Kalkulator Win-Rate & Rekam Jejak")
        with c_hb:
            refresh_hist = st.button("🔄 Refresh Jurnal", use_container_width=True)
            
        if refresh_hist or 'history_data' not in st.session_state:
            with st.spinner("Mengambil data Jurnal..."):
                hist_response = requests.post(GAS_URL, json={"action": "get_history", "username": st.session_state['username']}, allow_redirects=True)
                if hist_response.status_code == 200:
                    st.session_state['history_data'] = hist_response.json().get("data", [])
                    
        if 'history_data' in st.session_state:
            df_hist = pd.DataFrame(st.session_state['history_data'])
            if not df_hist.empty:
                tot_trades = len(df_hist)
                win_trades = len(df_hist[df_hist['Status'].str.contains("TP|RISK", case=False, na=False)])
                
                total_pnl_rp = 0
                for idx, row in df_hist.iterrows():
                    entry = float(row['Entry Price'])
                    live = float(row['Live Price'])
                    lot = float(row['Lot'])
                    pnl = (live - entry) * lot * 100
                    total_pnl_rp += pnl
                    df_hist.at[idx, 'Profit (Rp)'] = f"Rp {pnl:,.0f}"

                win_rate = (win_trades / tot_trades) * 100 if tot_trades > 0 else 0
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("⚖️ Total Trading", f"{tot_trades} Saham")
                m2.metric("🏆 Menang (TP)", f"{win_trades} Kali")
                m3.metric("🎯 Win Rate", f"{win_rate:.1f}%")
                m4.metric("💰 Total PnL", f"Rp {total_pnl_rp:,.0f}", delta="Profit" if total_pnl_rp > 0 else "Rugi", delta_color="normal" if total_pnl_rp > 0 else "inverse")
                
                st.markdown("---")
                df_hist_disp = df_hist.drop(columns=['Persentase_Num', 'Entry Price', 'Live Price'])
                st.dataframe(df_hist_disp, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("📡 Radar Screener (Momentum Teknikal & Volume)")
        st.markdown("Fitur ini memindai saham secara massal dan *real-time* untuk mendeteksi momentum teknikal (Trend & Lonjakan Volume) dalam hitungan detik.")
        
        saham_list = st.text_input("Daftar Kode Saham (Pisahkan dengan koma)", "BBCA, BBRI, BMRI, BBNI, TLKM, ASII, GOTO, BUMI, AMMN, BREN")
        if st.button("🚀 Mulai Radar Scan", use_container_width=True):
            with st.spinner("Memindai pasar..."):
                emiten_scan = [e.strip().upper() + ".JK" for e in saham_list.split(",")]
                hasil_scan = []
                
                for e in emiten_scan:
                    try:
                        df_emiten = yf.Ticker(e).history(period="1mo")
                        if not df_emiten.empty and len(df_emiten) > 2:
                            c_price = float(df_emiten['Close'].iloc[-1])
                            p_price = float(df_emiten['Close'].iloc[-2])
                            v_today = float(df_emiten['Volume'].iloc[-1])
                            v_mean = float(df_emiten['Volume'].mean())
                            
                            pct = ((c_price - p_price) / p_price) * 100
                            v_spike = v_today > (v_mean * 1.5)
                            trend = "UPTREND" if c_price > df_emiten['Close'].mean() else "DOWNTREND"
                            
                            status = "🔥 HOT (Beli)" if trend == "UPTREND" and v_spike and pct > 0 else "⏳ Pantau"
                            if trend == "DOWNTREND" and pct < 0: status = "🚨 Hindari"
                            
                            hasil_scan.append({
                                "Emiten": e.replace(".JK", ""),
                                "Live Price": c_price,
                                "Perubahan": f"{pct:.2f}%",
                                "Trend": trend,
                                "Volume": "Lonjakan Masif!" if v_spike else "Normal",
                                "Rekomendasi": status
                            })
                    except:
                        pass
                
                if hasil_scan:
                    df_scan = pd.DataFrame(hasil_scan)
                    def style_scan(val):
                        v = str(val)
                        if 'HOT' in v or 'Masif' in v or 'UPTREND' in v: return 'color: #2ecc71; font-weight:bold;'
                        if 'Hindari' in v or 'DOWNTREND' in v or '-' in v: return 'color: #e74c3c; font-weight:bold;'
                        if 'Pantau' in v or 'Normal' in v: return 'color: #f39c12; font-weight:bold;'
                        return ''
                    try: st.dataframe(df_scan.style.map(style_scan, subset=['Trend', 'Volume', 'Rekomendasi']), use_container_width=True, hide_index=True)
                    except: st.dataframe(df_scan.style.applymap(style_scan, subset=['Trend', 'Volume', 'Rekomendasi']), use_container_width=True, hide_index=True)
                else:
                    st.warning("Gagal memindai saham. Pastikan format kode benar dan terdaftar di bursa IHSG.")
