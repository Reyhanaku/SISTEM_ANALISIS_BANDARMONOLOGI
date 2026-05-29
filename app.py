import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistem Analisis ", page_icon="📈", layout="wide")

GAS_URL = "https://script.google.com/macros/s/AKfycbztzJL_waRDfHgmfgxLZN4em1N6RikwOBAvv7Q-9csLxWCOGAbFPUh219JAmP4Tgw/exec"

# ==========================================
# INISIALISASI SESSION STATE
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'brokers' not in st.session_state:
    st.session_state['brokers'] = []

# ==========================================
# HALAMAN LOGIN / REGISTER / LUPA PASSWORD
# ==========================================
if not st.session_state['logged_in']:
    st.title("🔐 Akses Sistem SPK Saham")
    
    # Membagi area menjadi 3 tab
    tab_login, tab_register, tab_forgot = st.tabs(["🔑 Masuk", "📝 Daftar Akun", "🆘 Lupa Password"])
    
    # --- TAB 1: LOGIN ---
    with tab_login:
        st.markdown("Silakan masuk jika Anda sudah memiliki akun.")
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Masuk", width='stretch')
            
            if submit_login:
                if not username_input or not password_input:
                    st.warning("Username dan Password wajib diisi!")
                else:
                    with st.spinner("Memverifikasi data..."):
                        payload = {"action": "login", "username": username_input, "password": password_input}
                        try:
                            res = requests.post(GAS_URL, json=payload, allow_redirects=True)
                            if res.status_code == 200:
                                data = res.json()
                                if data.get("status") == "success":
                                    st.session_state['logged_in'] = True
                                    st.session_state['username'] = username_input
                                    st.success("Login berhasil!")
                                    st.rerun()
                                else:
                                    st.error(data.get("message", "Gagal login."))
                            else:
                                st.error("Gagal terhubung ke database Spreadsheet.")
                        except Exception as e:
                            st.error("Terjadi kesalahan koneksi.")

    # --- TAB 2: DAFTAR MANDIRI ---
    with tab_register:
        st.markdown("Belum punya akun? Daftarkan diri Anda di sini secara gratis.")
        with st.form("register_form"):
            new_user = st.text_input("Buat Username")
            new_email = st.text_input("Alamat Email (Harus Aktif)")
            new_pass = st.text_input("Buat Password", type="password")
            conf_pass = st.text_input("Konfirmasi Password", type="password")
            submit_register = st.form_submit_button("Daftar Sekarang", width='stretch')
            
            if submit_register:
                if not new_user or not new_email or not new_pass:
                    st.warning("Semua kolom (Username, Email, Password) wajib diisi!")
                elif new_pass != conf_pass:
                    st.error("Password dan Konfirmasi Password tidak cocok!")
                else:
                    with st.spinner("Mendaftarkan akun..."):
                        payload = {"action": "register", "username": new_user, "password": new_pass, "email": new_email}
                        try:
                            res = requests.post(GAS_URL, json=payload, allow_redirects=True)
                            if res.status_code == 200:
                                data = res.json()
                                if data.get("status") == "success":
                                    st.success(data.get("message"))
                                else:
                                    st.error(data.get("message"))
                        except Exception as e:
                            st.error("Terjadi kesalahan koneksi saat mendaftar.")

    # --- TAB 3: LUPA PASSWORD ---
    with tab_forgot:
        st.markdown("Lupa password? Masukkan username Anda dan kami akan mengirimkan password ke email yang terdaftar.")
        with st.form("forgot_form"):
            f_user = st.text_input("Masukkan Username Anda")
            submit_forgot = st.form_submit_button("Kirim Password via Email", width='stretch')
            
            if submit_forgot:
                if not f_user:
                    st.warning("Username wajib diisi untuk mencari akun Anda!")
                else:
                    with st.spinner("Mencari akun dan mengirim email... (Mohon tunggu beberapa detik)"):
                        payload = {"action": "forgot_password", "username": f_user}
                        try:
                            res = requests.post(GAS_URL, json=payload, allow_redirects=True)
                            if res.status_code == 200:
                                data = res.json()
                                if data.get("status") == "success":
                                    st.success(data.get("message"))
                                else:
                                    st.error(data.get("message"))
                        except Exception as e:
                            st.error("Terjadi kesalahan koneksi.")

# ==========================================
# HALAMAN UTAMA (JIKA SUDAH LOGIN)
# ==========================================
else:
    # Tarik data broker jika kosong
    if not st.session_state['brokers']:
        try:
            res = requests.get(GAS_URL)
            if res.status_code == 200:
                st.session_state['brokers'] = res.json().get('brokers', [])
        except:
            st.session_state['brokers'] = []

    # Header dengan Tombol Logout
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("📊 Sistem Analisis Bandarmologi IHSG")
    with col_logout:
        st.write("") # Spacer vertikal
        if st.button("🚪 Logout", width='stretch'):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.rerun()

    st.markdown(f"Selamat datang, **{st.session_state['username']}**. Berikut adalah *dashboard trading* pribadi Anda.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["💰💰💰 Input Data & Analisis", "🎯 Dashboard Log Book"])

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
            st.markdown("**Buyers**")
            by1 = st.selectbox("Buyer 1", options=[""] + st.session_state['brokers'], key="b1")
            by2 = st.selectbox("Buyer 2", options=[""] + st.session_state['brokers'], key="b2")
            by3 = st.selectbox("Buyer 3", options=[""] + st.session_state['brokers'], key="b3")
            by4 = st.selectbox("Buyer 4", options=[""] + st.session_state['brokers'], key="b4")
            by5 = st.selectbox("Buyer 5", options=[""] + st.session_state['brokers'], key="b5")

        with col_sell:
            st.markdown("**Sellers**")
            sl1 = st.selectbox("Seller 1", options=[""] + st.session_state['brokers'], key="s1")
            sl2 = st.selectbox("Seller 2", options=[""] + st.session_state['brokers'], key="s2")
            sl3 = st.selectbox("Seller 3", options=[""] + st.session_state['brokers'], key="s3")
            sl4 = st.selectbox("Seller 4", options=[""] + st.session_state['brokers'], key="s4")
            sl5 = st.selectbox("Seller 5", options=[""] + st.session_state['brokers'], key="s5")

        if st.button("🚀 Proses Data ke Sistem", width='stretch'):
            if not emiten:
                st.warning("Kode Emiten wajib diisi!")
            else:
                with st.spinner("Memproses data ke Spreadsheet... (Mohon tunggu)"):
                    payload = {
                        "action": "input_data", "emiten": emiten, "total_net_buy": total_net_buy,
                        "by1": by1, "by2": by2, "by3": by3, "by4": by4, "by5": by5,
                        "sl1": sl1, "sl2": sl2, "sl3": sl3, "sl4": sl4, "sl5": sl5
                    }
                    try:
                        response = requests.post(GAS_URL, json=payload, allow_redirects=True)
                        if response.status_code == 200 and "success" in response.text:
                            st.session_state['hasil_analisis'] = response.json()
                            st.session_state['emiten'] = emiten
                            st.success(f"Data {emiten} berhasil diproses!")
                        else:
                            st.error("Gagal memproses data ke Spreadsheet.")
                    except Exception as e:
                        st.error("Gagal terhubung ke server.")

        if 'hasil_analisis' in st.session_state:
            st.markdown("---")
            res = st.session_state['hasil_analisis']
            
            st.subheader(f"💡 Hasil Analisis: {st.session_state['emiten']}")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Scor Beli Bandar", f"{res.get('scor_beli', 0)}")
            kpi2.metric("Scor Jual Ritel", f"{res.get('scor_jual', 0)}")
            kpi3.metric("Status SPK", res.get('status_spk', '-'))
            kpi4.metric("Grade", res.get('grade', '-'))

            st.write("### Trading Plan Screener")
            tp1, tp2, tp3, tp4, tp5 = st.columns(5)
            tp1.metric("Entry Price", res.get('entry_price', 0))
            tp2.metric("Target Price 1", res.get('tp1', 0))
            tp3.metric("Target Price 2", res.get('tp2', 0))
            tp4.metric("Target Price 3", res.get('tp3', 0))
            tp5.metric("Cutloss Price", res.get('cutloss', 0))

            st.markdown("---")
            st.subheader("📒 Simpan ke Log Book")
            with st.form("log_book_form"):
                tanggal = st.date_input("Tanggal Pantauan", datetime.today())
                submit_log = st.form_submit_button("Simpan Data ke Log Book", width='stretch')

                if submit_log:
                    with st.spinner("Menyimpan ke Log Book..."):
                        log_payload = {
                            "action": "save_logbook", 
                            "username": st.session_state['username'], 
                            "emiten": st.session_state['emiten'],
                            "entry_price": res.get('entry_price', 0), "tp1": res.get('tp1', 0),
                            "tp2": res.get('tp2', 0), "tp3": res.get('tp3', 0),
                            "cutloss": res.get('cutloss', 0), "grade": res.get('grade', '-'),
                            "tanggal": tanggal.strftime("%Y-%m-%d")
                        }
                        try:
                            response_log = requests.post(GAS_URL, json=log_payload, allow_redirects=True)
                            if response_log.status_code == 200 and "success" in response_log.text:
                                st.success(f"Trading plan {st.session_state['emiten']} berhasil dicatat di Log Book!")
                            else:
                                st.error("Gagal menyimpan ke Log Book.")
                        except Exception as e:
                            st.error("Gagal terhubung ke server.")

    with tab2:
        col_title, col_btn = st.columns([3, 1])
        with col_title:
            st.subheader("Tabel Pantauan Saham Aktif")
        with col_btn:
            refresh = st.button("🔄 Refresh Data", width='stretch')
            
        if refresh or 'logbook_data' not in st.session_state:
            with st.spinner("Mengambil data Log Book terbaru..."):
                try:
                    logbook_response = requests.post(GAS_URL, json={"action": "get_logbook", "username": st.session_state['username']}, allow_redirects=True)
                    if logbook_response.status_code == 200:
                        data_json = logbook_response.json()
                        if data_json.get("status") == "success":
                            st.session_state['logbook_data'] = data_json.get("data", [])
                        else:
                            st.error("Gagal memuat data dari Spreadsheet.")
                except Exception as e:
                    st.error("Terjadi kesalahan koneksi saat mengambil data.")
        
        if 'logbook_data' in st.session_state:
            df_logbook = pd.DataFrame(st.session_state['logbook_data'])
            
            if not df_logbook.empty:
                total_saham = len(df_logbook)
                hold_count = len(df_logbook[df_logbook['Status'].astype(str).str.contains("HOLD", case=False, na=False)])
                tp_count = len(df_logbook[df_logbook['Status'].astype(str).str.contains("TP", case=False, na=False)])
                cl_count = len(df_logbook[df_logbook['Status'].astype(str).str.contains("CUTLOSS", case=False, na=False)])
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("📌 Total Emiten", total_saham)
                m2.metric("⏳ Status HOLD", hold_count)
                m3.metric("🚀 Kena TP", tp_count)
                m4.metric("🚨 Kena Cutloss", cl_count)
                
                st.markdown("---")
                
                f1, f2 = st.columns(2)
                with f1:
                    search_query = st.text_input("🔍 Cari Kode Emiten", "")
                with f2:
                    status_filter = st.selectbox("📂 Filter Status", ["Semua", "HOLD", "TP", "CUTLOSS"])
                    
                if search_query:
                    df_logbook = df_logbook[df_logbook['Emiten'].astype(str).str.contains(search_query.upper(), na=False)]
                if status_filter != "Semua":
                    df_logbook = df_logbook[df_logbook['Status'].astype(str).str.contains(status_filter, case=False, na=False)]
                
                def style_dataframe(df):
                    def highlight_status(val):
                        val_str = str(val).upper()
                        if 'TP' in val_str:
                            return 'background-color: rgba(39, 174, 96, 0.2); color: #2ecc71; font-weight: bold;'
                        elif 'CUTLOSS' in val_str:
                            return 'background-color: rgba(192, 57, 43, 0.2); color: #e74c3c; font-weight: bold;'
                        elif 'HOLD' in val_str:
                            return 'color: #f39c12; font-weight: bold;'
                        return ''

                    def highlight_persentase(val):
                        val_str = str(val)
                        if '-' in val_str:
                            return 'color: #e74c3c; font-weight: bold;'
                        elif val_str.strip() != '' and val_str != 'nan':
                            return 'color: #2ecc71; font-weight: bold;'
                        return ''
                    
                    try:
                        return df.style.map(highlight_status, subset=['Status']).map(highlight_persentase, subset=['Persentase'])
                    except AttributeError:
                        return df.style.applymap(highlight_status, subset=['Status']).applymap(highlight_persentase, subset=['Persentase'])

                st.dataframe(style_dataframe(df_logbook), width='stretch', hide_index=True, height=500)
                
            else:
                st.info("📂 Log Book Anda masih kosong. Hasil simpangan Anda akan masuk kemari dan 100% aman (privat).")
