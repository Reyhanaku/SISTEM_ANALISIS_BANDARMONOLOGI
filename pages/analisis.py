import streamlit as st
from datetime import datetime
from utils.api import fetch_brokers, post_data

def render_analisis():
    st.subheader("Input Data Analisis")
    brokers = fetch_brokers()
    
    col_emiten, col_net = st.columns(2)
    with col_emiten:
        emiten = st.text_input("Kode Emiten").upper()
    with col_net:
        total_net_buy = st.number_input("Total Net Buy", min_value=0.0, format="%.2f")

    st.write("### Top 5 Buyers & Sellers")
    col_buy, col_sell = st.columns(2)
    with col_buy:
        st.markdown("**Buyers**")
        by1 = st.selectbox("Buyer 1", options=[""] + brokers, key="b1")
        by2 = st.selectbox("Buyer 2", options=[""] + brokers, key="b2")
        by3 = st.selectbox("Buyer 3", options=[""] + brokers, key="b3")
        by4 = st.selectbox("Buyer 4", options=[""] + brokers, key="b4")
        by5 = st.selectbox("Buyer 5", options=[""] + brokers, key="b5")
    with col_sell:
        st.markdown("**Sellers**")
        sl1 = st.selectbox("Seller 1", options=[""] + brokers, key="s1")
        sl2 = st.selectbox("Seller 2", options=[""] + brokers, key="s2")
        sl3 = st.selectbox("Seller 3", options=[""] + brokers, key="s3")
        sl4 = st.selectbox("Seller 4", options=[""] + brokers, key="s4")
        sl5 = st.selectbox("Seller 5", options=[""] + brokers, key="s5")

    if st.button("🚀 Proses Data ke Sistem", width='stretch'):
        if not emiten:
            st.warning("Kode Emiten wajib diisi!")
        else:
            with st.spinner("Memproses data..."):
                payload = {
                    "action": "input_data", "emiten": emiten, "total_net_buy": total_net_buy,
                    "by1": by1, "by2": by2, "by3": by3, "by4": by4, "by5": by5,
                    "sl1": sl1, "sl2": sl2, "sl3": sl3, "sl4": sl4, "sl5": sl5
                }
                res = post_data(payload)
                if res and res.get("status") == "success":
                    st.session_state['hasil_analisis'] = res
                    st.session_state['emiten'] = emiten
                    st.success(f"Data {emiten} berhasil diproses!")
                else:
                    st.error("Gagal memproses data.")

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
        tp2.metric("TP 1", res.get('tp1', 0))
        tp3.metric("TP 2", res.get('tp2', 0))
        tp4.metric("TP 3", res.get('tp3', 0))
        tp5.metric("Cutloss", res.get('cutloss', 0))

        st.markdown("---")
        st.subheader("📒 Simpan ke Log Book")
        with st.form("log_book_form"):
            tanggal = st.date_input("Tanggal Pantauan", datetime.today())
            if st.form_submit_button("Simpan Data ke Log Book", width='stretch'):
                with st.spinner("Menyimpan..."):
                    log_payload = {
                        "action": "save_logbook", "username": st.session_state['username'],
                        "emiten": st.session_state['emiten'], "entry_price": res.get('entry_price', 0),
                        "tp1": res.get('tp1', 0), "tp2": res.get('tp2', 0), "tp3": res.get('tp3', 0),
                        "cutloss": res.get('cutloss', 0), "grade": res.get('grade', '-'),
                        "tanggal": tanggal.strftime("%Y-%m-%d")
                    }
                    res_log = post_data(log_payload)
                    if res_log and res_log.get("status") == "success":
                        st.success("Berhasil dicatat di Log Book!")
                    else:
                        st.error("Gagal menyimpan.")