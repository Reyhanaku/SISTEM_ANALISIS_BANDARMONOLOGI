import streamlit as st
import pandas as pd
from utils.api import post_data
from utils.market import get_live_price

def style_dataframe(df):
    def highlight_status(val):
        val_str = str(val).upper()
        if 'TP' in val_str: return 'background-color: rgba(39,174,96,0.1); color: #2ecc71; font-weight: bold;'
        elif 'CUTLOSS' in val_str: return 'background-color: rgba(192,57,43,0.1); color: #e74c3c; font-weight: bold;'
        elif 'HOLD' in val_str: return 'color: #f39c12; font-weight: bold;'
        return ''
    
    def highlight_persentase(val):
        val_str = str(val)
        if '-' in val_str: return 'color: #e74c3c; font-weight: bold;'
        elif val_str.strip() != '' and val_str != 'nan': return 'color: #2ecc71; font-weight: bold;'
        return ''
    
    try:
        return df.style.map(highlight_status, subset=['Status']).map(highlight_persentase, subset=['Persentase'])
    except:
        return df.style.applymap(highlight_status, subset=['Status']).applymap(highlight_persentase, subset=['Persentase'])

def render_logbook():
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.subheader("Tabel Pantauan Saham Aktif")
    with col_btn:
        refresh = st.button("🔄 Refresh Data", width='stretch')
        
    if refresh or 'logbook_data' not in st.session_state:
        with st.spinner("Menarik data Log Book..."):
            res = post_data({"action": "get_logbook", "username": st.session_state['username']})
            if res and res.get("status") == "success":
                st.session_state['logbook_data'] = res.get("data", [])
            else:
                st.error("Gagal memuat data.")

    if 'logbook_data' in st.session_state:
        df_logbook = pd.DataFrame(st.session_state['logbook_data'])
        if not df_logbook.empty:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("📌 Total Emiten", len(df_logbook))
            m2.metric("⏳ Status HOLD", len(df_logbook[df_logbook['Status'].astype(str).str.contains("HOLD")]))
            m3.metric("🚀 Kena TP", len(df_logbook[df_logbook['Status'].astype(str).str.contains("TP")]))
            m4.metric("🚨 Kena Cutloss", len(df_logbook[df_logbook['Status'].astype(str).str.contains("CUTLOSS")]))
            
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

            st.dataframe(style_dataframe(df_logbook), width='stretch', hide_index=True, height=400)
            
            st.markdown("---")
            st.subheader("🗑 Hapus Data Log Book")
            emiten_list = df_logbook['Emiten'].tolist()
            if emiten_list:
                del_emiten = st.selectbox("Pilih Emiten yang ingin dihapus:", emiten_list)
                if st.button("Hapus Emiten", width='stretch'):
                    with st.spinner("Menghapus data..."):
                        res_del = post_data({"action": "delete_logbook", "username": st.session_state['username'], "emiten": del_emiten})
                        if res_del and res_del.get("status") == "success":
                            st.success(f"{del_emiten} dihapus!")
                            st.session_state.pop('logbook_data', None)
                            st.rerun()
                        else:
                            st.error("Gagal menghapus.")
        else:
            st.info("📂 Log Book Anda masih kosong.")