import streamlit as st
from utils.api import post_data

def render_auth():
    st.title("🔐 Akses Dasbor Trading VIP")
    
    tab_login, tab_register, tab_forgot = st.tabs(["🔑 Masuk", "📝 Daftar Baru", "🆘 Reset Password"])
    
    with tab_login:
        st.markdown("Selamat datang kembali! Masuk untuk amankan portofolio kamu.")
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            if st.form_submit_button("Masuk", width='stretch'):
                if not username_input or not password_input:
                    st.warning("Username dan Password wajib diisi!")
                else:
                    with st.spinner("Memverifikasi data..."):
                        res = post_data({"action": "login", "username": username_input, "password": password_input})
                        if res and res.get("status") == "success":
                            st.session_state['logged_in'] = True
                            st.session_state['username'] = username_input
                            st.rerun()
                        else:
                            st.error(res.get("message", "Gagal login.") if res else "Koneksi Error.")

    with tab_register:
        st.markdown("Mulai trading lebih pintar. Registrasi akun kamu di sini (100% Free).")
        with st.form("register_form"):
            new_user = st.text_input("Buat Username")
            new_email = st.text_input("Alamat Email (Harus Aktif)")
            new_pass = st.text_input("Buat Password", type="password")
            conf_pass = st.text_input("Konfirmasi Password", type="password")
            if st.form_submit_button("Daftar Sekarang", width='stretch'):
                if not new_user or not new_email or not new_pass:
                    st.warning("Semua kolom wajib diisi!")
                elif new_pass != conf_pass:
                    st.error("Password tidak cocok!")
                else:
                    with st.spinner("Mendaftarkan akun..."):
                        res = post_data({"action": "register", "username": new_user, "password": new_pass, "email": new_email})
                        if res and res.get("status") == "success":
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message", "Gagal mendaftar.") if res else "Koneksi Error.")

    with tab_forgot:
        st.markdown("Lupa password itu wajar. Kasih tahu username kamu, biar sistem yang urus sisanya.")
        with st.form("forgot_form"):
            f_user = st.text_input("Masukkan Username Anda")
            if st.form_submit_button("Kirim Password via Email", width='stretch'):
                if not f_user:
                    st.warning("Username wajib diisi!")
                else:
                    with st.spinner("Mencari akun dan mengirim email..."):
                        res = post_data({"action": "forgot_password", "username": f_user})
                        if res and res.get("status") == "success":
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("message", "Gagal mengirim.") if res else "Koneksi Error.")