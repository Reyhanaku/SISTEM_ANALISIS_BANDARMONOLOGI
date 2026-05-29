import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import yfinance as yf

st.set_page_config(page_title="Sistem Analisis", page_icon="🎯", layout="wide")

# ==============================================================
GAS_URL = "https://script.google.com/macros/s/AKfycbztzJL_waRDfHgmfgxLZN4em1N6RikwOBAvv7Q-9csLxWCOGAbFPUh219JAmP4Tgw/exec"
# ==============================================================

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'brokers' not in st.session_state:
    st.session_state['brokers'] = []

# --- HALAMAN LOGIN ---
if not st.session_state['logged_in']:
    st.title("🔐 Akses Sistem SPK Saham")
    tab_login, tab_register, tab_forgot = st.tabs(["🔑 Masuk", "📝 Daftar Akun", "🆘 Lupa Password"])
    
    with tab_login:
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Masuk", width='stretch')
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
                    except: st.error("Gagal terhubung.")
                            
    with tab_register:
        with st.form("register_form"):
            new_user, new_email, new_pass, conf_pass = st.text_input("Buat Username"), st.text_input("Alamat Email"), st.text_input("Buat Password", type="password"), st.text_input("Konfirmasi Password", type="password")
            if st.form_submit_button("Daftar Sekarang", width='stretch'):
                if new_pass != conf_pass: st.error("Password tidak cocok!")
                else:
                    try:
                        res = requests.post(GAS_URL, json={"action": "register", "username": new_user, "password": new_pass, "email": new_email}, allow_redirects=True)
                        st.success(res.json().get("message"))
                    except: st.error("Gagal mendaftar.")
                            
    with tab_forgot:
        with st.form("forgot_form"):
            f_user = st.text_input("Masukkan Username Anda")
            if st.form_submit_button("Kirim Password via Email", width='stretch'):
                try:
                    res = requests.post(GAS_URL, json={"action": "forgot_password", "username": f_user}, allow_redirects=True)
                    st.success(res.json().get("message"))
                except: st.error("Gagal mengirim.")

# --- DASHBOARD UTAMA ---
else:
    if not st.session_state['brokers']:
        try:
            res = requests.get(GAS_URL)
            if res.status_code == 200: st.session_state['brokers'] = res.json().get('brokers', [])
        except: st.session_state['brokers'] = []
            
    col_title, col_logout = st.columns([5, 1])
    with col_title: st.title("🎯 Sistem Analisis Bandarmologi IHSG")
    with col_logout:
        st.write("")
        if st.button("🚪 Logout", width='stretch'):
            st.session_state['logged_in'] = False
            st.rerun()
            
    st.markdown(f"Selamat datang, **{st.session_state['username']}**. Berikut adalah dashboard trading pribadi Anda.")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["💰 Input Data & Analisis", "🎯 Dashboard Log Book", "🏆 Jurnal & Performa"])
    
    # --- TAB 1: INPUT DATA ---
    with tab1:
        st.subheader("Input Data Analisis")
        col_emiten, col_net = st.columns(2)
        with col_emiten: emiten = st.text_input("Kode Emiten").upper()
        with col_net: total_net_buy = st.number_input("Total Net Buy", min_value=0.0, format="%.2f")
            
        st.write("### Top 5 Buyers & Sellers")
        col_buy, col_sell = st.columns(2)
        with col_buy:
            b1, b2, b3, b4, b5 = [st.selectbox(f"Buyer {i}", [""] + st.session_state['brokers'], key=f"b{i}") for i in range(1, 6)]
        with col_sell:
            s1, s2, s3, s4, s5 = [st.selectbox(f"Seller {i}", [""] + st.session_state['brokers'], key=f"s{i}") for i in range(1, 6)]
            
        if st.button("🚀 Proses Data ke Sistem", width='stretch'):
            if emiten:
                with st.spinner("Memproses data..."):
                    payload = {"action": "input_data", "emiten": emiten, "total_net_buy": total_net_buy, "by1": b1, "by2": b2, "by3": b3, "by4": b4, "by5": b5, "sl1": s1, "sl2": s2, "sl3": s3, "sl4": s4, "sl5": s5}
                    try:
                        res = requests.post(GAS_URL, json=payload, allow_redirects=True)
                        if res.status_code == 200:
                            st.session_state['hasil_analisis'] = res.json()
                            st.session_state['emiten'] = emiten
                            st.success(f"Data {emiten} berhasil diproses!")
                    except: st.error("Gagal terhubung.")
                        
        if 'hasil_analisis' in st.session_state:
            res = st.session_state['hasil_analisis']
            st.markdown("---")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Scor Beli", res.get('scor_beli', 0)); k2.metric("Scor Jual", res.get('scor_jual', 0))
            k3.metric("Status SPK", res.get('status_spk', '-')); k4.metric("Grade", res.get('grade', '-'))
            
            st.write("### Trading Plan")
            t1, t2, t3, t4, t5 = st.columns(5)
            t1.metric("Entry", res.get('entry_price', 0)); t2.metric("TP 1", res.get('tp1', 0))
            t3.metric("TP 2", res.get('tp2', 0)); t4.metric("TP 3", res.get('tp3', 0)); t5.metric("Cutloss", res.get('cutloss', 0))
            
            st.markdown("---")
            with st.form("log_book_form"):
                col_tgl, col_lot = st.columns(2)
                with col_tgl: tanggal = st.date_input("Tanggal Pantauan", datetime.today())
                with col_lot: lot_beli = st.number_input("Jumlah Lot", min_value=1, step=1, value=10) # MONEY MANAGEMENT FITUR
                
                if st.form_submit_button("Simpan ke Log Book", width='stretch'):
                    payload = {
                        "action": "save_logbook", "username": st.session_state['username'], "emiten": st.session_state['emiten'],
                        "entry_price": res.get('entry_price', 0), "tp1": res.get('tp1', 0), "tp2": res.get('tp2', 0),
                        "tp3": res.get('tp3', 0), "cutloss": res.get('cutloss', 0), "grade": res.get('grade', '-'),
                        "tanggal": tanggal.strftime("%Y-%m-%d"), "lot": lot_beli
                    }
                    try:
                        if requests.post(GAS_URL, json=payload, allow_redirects=True).status_code == 200:
                            st.success("Tersimpan di Log Book!")
                    except: st.error("Gagal menyimpan.")

    # --- TAB 2: DASHBOARD LOG BOOK ---
    with tab2:
        c_title, c_btn = st.columns([3, 1])
        with c_title: st.subheader("Pantauan Portofolio Aktif")
        with c_btn: refresh = st.button("🔄 Refresh Harga Real-Time", width='stretch')
            
        if refresh or 'logbook_data' not in st.session_state:
            with st.spinner("Mengambil harga instan dari market..."):
                try:
                    log_res = requests.post(GAS_URL, json={"action": "get_logbook", "username": st.session_state['username']}, allow_redirects=True)
                    if log_res.status_code == 200:
                        raw_data = log_res.json().get("data", [])
                        
                        # FITUR BYPASS REAL-TIME & TRAILING STOP
                        if raw_data:
                            emiten_list = [d["Emiten"] + ".JK" for d in raw_data]
                            market_data = yf.download(emiten_list, period="1d", group_by="ticker", threads=True, progress=False)
                            
                            for row in raw_data:
                                em_code = row["Emiten"] + ".JK"
                                try:
                                    if len(emiten_list) == 1: live_price = float(market_data['Close'].iloc[-1])
                                    else: live_price = float(market_data[em_code]['Close'].iloc[-1])
                                except: live_price = float(row["Live Price"] if row["Live Price"] else 0) # Failsafe
                                
                                row["Live Price"] = live_price
                                entry = float(row["Entry Price"])
                                lot = float(row["Lot"])
                                tp1 = float(row["TP 1"])
                                tp3 = float(row["TP 3"])
                                cl = float(row["Cutloss Price"])
                                
                                # Kalkulasi Rp
                                pnl_rp = (live_price - entry) * lot * 100
                                row["Profit (Rp)"] = f"Rp {pnl_rp:,.0f}"
                                row["Persentase"] = f"{((live_price - entry) / entry * 100):.2f}%" if entry > 0 else "0%"
                                
                                # Trailing Stop Logic
                                if live_price >= tp3: row["Status"] = "🚀 TP 3 HIT!"
                                elif live_price >= float(row["TP 2"]): row["Status"] = "🔥 TP 2 HIT!"
                                elif live_price >= tp1: row["Status"] = "🛡️ RISK-FREE" # FITUR TRAILING STOP
                                elif live_price <= cl: row["Status"] = "🚨 CUTLOSS!"
                                else: row["Status"] = "⏳ HOLD"
                                
                        st.session_state['logbook_data'] = raw_data
                except Exception as e: st.error("Kesalahan jaringan.")
                    
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
                        
                st.dataframe(style_df(df_logbook), width='stretch', hide_index=True)
                st.markdown("---")
                
                # FITUR MANAJEMEN: EDIT & HAPUS
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
                            if st.button("Update Data", width='stretch'):
                                with st.spinner("Menyimpan..."):
                                    payload = {"action": "update_logbook", "username": st.session_state['username'], "emiten": edit_em, "entry_price": new_entry, "lot": new_lot, "tp1": new_tp1, "tp2": new_tp2, "tp3": new_tp3, "cutloss": new_cl}
                                    requests.post(GAS_URL, json=payload)
                                    st.session_state.pop('logbook_data', None)
                                    st.rerun()

                with c2:
                    st.markdown("#### 🏆 Selesai Trading")
                    move_em = st.selectbox("Arsipkan ke Jurnal", emiten_list, key="mv")
                    if st.button("Pindah ke Jurnal", width='stretch', type='primary'):
                        with st.spinner("Memindahkan..."):
                            requests.post(GAS_URL, json={"action": "move_to_history", "username": st.session_state['username'], "emiten": move_em})
                            st.session_state.pop('logbook_data', None); st.session_state.pop('history_data', None)
                            st.rerun()

                with c3:
                    st.markdown("#### 🗑 Hapus Data")
                    del_em = st.selectbox("Hapus Permanen", emiten_list, key="dl")
                    if st.button("Hapus Emiten", width='stretch'):
                        with st.spinner("Menghapus..."):
                            requests.post(GAS_URL, json={"action": "delete_logbook", "username": st.session_state['username'], "emiten": del_em})
                            st.session_state.pop('logbook_data', None)
                            st.rerun()

    # --- TAB 3: JURNAL & PERFORMA ---
    with tab3:
        c_ht, c_hb = st.columns([3, 1])
        with c_ht: st.subheader("Kalkulator Win-Rate & Rekam Jejak")
        with c_hb: refresh_hist = st.button("🔄 Refresh Jurnal", width='stretch')
            
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
                loss_trades = len(df_hist[df_hist['Status'].str.contains("CUTLOSS", case=False, na=False)])
                
                # Kalkulasi Rp di History
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
                m4.metric("💰 Total PnL (Rupiah)", f"Rp {total_pnl_rp:,.0f}", delta="Profit Bersih" if total_pnl_rp > 0 else "Rugi", delta_color="normal" if total_pnl_rp > 0 else "inverse")
                
                st.markdown("---")
                df_hist_disp = df_hist.drop(columns=['Persentase_Num', 'Entry Price', 'Live Price'])
                st.dataframe(df_hist_disp, width='stretch', hide_index=True)
