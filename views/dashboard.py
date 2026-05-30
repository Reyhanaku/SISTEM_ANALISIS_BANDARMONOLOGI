import streamlit as st
from datetime import datetime
from utils.api import fetch_brokers, post_data
from utils.market import get_historical_data
from components.charts import render_candlestick

def render():
    # 1. FORM INPUT DIBUAT RINGKAS (EXPANDER)
    with st.expander("📝 Form Input Data Bandarmologi", expanded=True):
        brokers = fetch_brokers()
        
        col_emiten, col_net = st.columns(2)
        with col_emiten:
            emiten = st.text_input("Kode Emiten (Cth: BBCA)").upper()
        with col_net:
            total_net_buy = st.number_input("Total Net Buy (Miliar)", min_value=0.0, format="%.2f")

        st.markdown("<p style='color:#94a3b8; margin-bottom:5px;'>Top 5 Buyers & Sellers</p>", unsafe_allow_html=True)
        col_buy, col_sell = st.columns(2)
        with col_buy:
            by1 = st.selectbox("Buyer 1", options=[""] + brokers, key="b1")
            by2 = st.selectbox("Buyer 2", options=[""] + brokers, key="b2")
            by3 = st.selectbox("Buyer 3", options=[""] + brokers, key="b3")
            by4 = st.selectbox("Buyer 4", options=[""] + brokers, key="b4")
            by5 = st.selectbox("Buyer 5", options=[""] + brokers, key="b5")
        with col_sell:
            sl1 = st.selectbox("Seller 1", options=[""] + brokers, key="s1")
            sl2 = st.selectbox("Seller 2", options=[""] + brokers, key="s2")
            sl3 = st.selectbox("Seller 3", options=[""] + brokers, key="s3")
            sl4 = st.selectbox("Seller 4", options=[""] + brokers, key="s4")
            sl5 = st.selectbox("Seller 5", options=[""] + brokers, key="s5")

        if st.button("🚀 Eksekusi Algoritma", width='stretch'):
            if not emiten:
                st.warning("Kode Emiten wajib diisi!")
            else:
                with st.spinner("Mesin sedang mengalkulasi data..."):
                    payload = {
                        "action": "input_data", "emiten": emiten, "total_net_buy": total_net_buy,
                        "by1": by1, "by2": by2, "by3": by3, "by4": by4, "by5": by5,
                        "sl1": sl1, "sl2": sl2, "sl3": sl3, "sl4": sl4, "sl5": sl5
                    }
                    res = post_data(payload)
                    if res and res.get("status") == "success":
                        st.session_state['hasil_analisis'] = res
                        st.session_state['emiten'] = emiten
                        st.success(f"Sinyal {emiten} berhasil di-generate!")
                    else:
                        st.error("Gagal memproses data.")

    # 2. HASIL ANALISIS DITAMPILKAN MEWAH
    if 'hasil_analisis' in st.session_state:
        res = st.session_state['hasil_analisis']
        emiten_aktif = st.session_state['emiten']
        
        st.markdown(f"<h3 style='margin-top:20px;'>💡 Trading Intelligence: <span style='color:#3b82f6;'>{emiten_aktif}</span></h3>", unsafe_allow_html=True)
        
        # --- TAMBAHAN: INDIKATOR SINYAL BUY / SELL OTOMATIS ---
        try:
            s_beli = float(res.get('scor_beli', 0))
            s_jual = float(res.get('scor_jual', 0))
        except ValueError:
            s_beli, s_jual = 0, 0
            
        if s_jual > s_beli:
            st.error(f"🚨 **SINYAL SELL (DISTRIBUSI):** Skor Jual/Distribusi ({s_jual}) mendominasi Skor Beli ({s_beli}). **Hindari masuk atau amankan profit jika sudah punya!**")
        elif s_beli > s_jual:
            st.success(f"🚀 **SINYAL BUY (AKUMULASI):** Skor Beli ({s_beli}) mendominasi Skor Jual ({s_jual}). **Bandar sedang kumpulin barang!**")
        else:
            st.warning(f"⚖️ **SINYAL NETRAL:** Tekanan Beli ({s_beli}) dan Jual ({s_jual}) seimbang. **Wait & See.**")
        st.markdown("---")
        # --------------------------------------------------------
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Scor Beli Bandar", f"{res.get('scor_beli', 0)}")
        kpi2.metric("Scor Jual Ritel", f"{res.get('scor_jual', 0)}") # Note: Di kode awal Anda teksnya "Scor Jual Ritel", saya biarkan sama.
        kpi3.metric("Status SPK", res.get('status_spk', '-'))
        kpi4.metric("Grade", res.get('grade', '-'))

        st.markdown("#### 🎯 Trading Plan & Target")
        tp1, tp2, tp3, tp4, tp5 = st.columns(5)
        tp1.metric("Entry Price", res.get('entry_price', 0))
        tp2.metric("TP 1", res.get('tp1', 0))
        tp3.metric("TP 2", res.get('tp2', 0))
        tp4.metric("TP 3", res.get('tp3', 0))
        tp5.metric("Cutloss", res.get('cutloss', 0))

        st.markdown("---")
        df_chart = get_historical_data(emiten_aktif)
        render_candlestick(df_chart, emiten_aktif)

        st.markdown("---")
        # FORM SIMPAN LOGBOOK DI DALAM EXPANDER (Agar rapi saat tidak dipakai)
        with st.expander("💼 Eksekusi & Simpan ke Portofolio (Money Management)", expanded=False):
            with st.form("log_book_form"):
                col_tgl, col_lot = st.columns(2)
                with col_tgl:
                    tanggal = st.date_input("Tanggal Transaksi", datetime.today())
                with col_lot:
                    lot_input = st.number_input("Volume (Jumlah Lot)", min_value=1, value=10)
                    
                if st.form_submit_button("Amankan ke Jurnal Trading", width='stretch'):
                    with st.spinner("Menyimpan ke brankas data..."):
                        log_payload = {
                            "action": "save_logbook", 
                            "username": st.session_state['username'], 
                            "emiten": emiten_aktif,
                            "entry_price": res.get('entry_price', 0), 
                            "tp1": res.get('tp1', 0), "tp2": res.get('tp2', 0), "tp3": res.get('tp3', 0),
                            "cutloss": res.get('cutloss', 0), 
                            "grade": res.get('grade', '-'),
                            "tanggal": tanggal.strftime("%Y-%m-%d"),
                            "lot": lot_input
                        }
                        res_log = post_data(log_payload)
                        if res_log and res_log.get("status") == "success":
                            st.success(f"Plan {emiten_aktif} berhasil masuk ke Portofolio Live!")
                        else:
                            st.error("Gagal menyimpan ke Log Book.")
