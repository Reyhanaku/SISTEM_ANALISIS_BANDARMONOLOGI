import streamlit as st
import pandas as pd
from utils.api import post_data

def format_rupiah(val):
    try:
        val = float(val)
        if val > 0:
            return f"+ Rp {val:,.0f}".replace(",", ".")
        elif val < 0:
            return f"- Rp {abs(val):,.0f}".replace(",", ".")
        else:
            return "Rp 0"
    except:
        return val

# --- FUNGSI BARU UNTUK MERAPIKAN TANGGAL & PERSEN ---
def clean_dataframe_format(df):
    # 1. Format Tanggal menjadi DD/MM/YYYY
    for col in ['Tanggal', 'Tanggal Hit']:
        if col in df.columns:
            # Jika isinya berupa "-", akan diabaikan dan tetap menjadi "-"
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y').fillna(df[col])
            
    # 2. Format Persentase Desimal menjadi %
    if 'Persentase' in df.columns:
        def format_persen(val):
            try:
                if pd.isna(val) or val == "": return ""
                if isinstance(val, str) and '%' in val: return val
                return f"{float(val) * 100:.2f}%"
            except:
                return str(val)
        df['Persentase'] = df['Persentase'].apply(format_persen)
        
    return df

def style_dataframe(df):
    def highlight_status(val):
        val_str = str(val).upper()
        if 'TP' in val_str: 
            return 'background-color: rgba(39, 174, 96, 0.2); color: #2ecc71; font-weight: bold;'
        elif 'CUTLOSS' in val_str: 
            return 'background-color: rgba(192, 57, 43, 0.2); color: #e74c3c; font-weight: bold;'
        elif 'HOLD' in val_str: 
            return 'color: #f39c12; font-weight: bold;'
        elif 'RISK-FREE' in val_str or '🛡' in val_str:
            return 'background-color: rgba(52, 152, 219, 0.2); color: #3498db; font-weight: bold;'
        return ''

    def highlight_persentase(val):
        val_str = str(val)
        if '-' in val_str: return 'color: #e74c3c; font-weight: bold;'
        elif val_str.strip() != '' and val_str != 'nan': return 'color: #2ecc71; font-weight: bold;'
        return ''
        
    def highlight_pnl(val):
        if isinstance(val, str):
            if val.startswith('+'): return 'color: #2ecc71; font-weight: bold;'
            elif val.startswith('-'): return 'color: #e74c3c; font-weight: bold;'
        return ''

    styler = df.style
    
    # Menyesuaikan dengan versi Pandas terbaru (map) atau lama (applymap)
    if hasattr(styler, 'map'):
        apply_func = styler.map
    else:
        apply_func = styler.applymap

    # PERBAIKAN: Hanya mengaplikasikan style jika kolomnya benar-benar ada di DataFrame
    if 'Status' in df.columns:
        styler = apply_func(highlight_status, subset=['Status'])
    if 'Persentase' in df.columns:
        styler = apply_func(highlight_persentase, subset=['Persentase'])
    if 'Floating Profit' in df.columns:
        styler = apply_func(highlight_pnl, subset=['Floating Profit'])

    return styler

def render():
    tab_log, tab_hist = st.tabs(["💼 Live Portofolio", "🏆 Histori & Win-Rate"])
    
    with tab_log:
        col_title, col_btn = st.columns([4, 1])
        with col_title:
            st.markdown("### 📊 Live Portofolio Tracking")
        with col_btn:
            refresh = st.button("🔄 Sync Market", width='stretch')
            
        if refresh or 'logbook_data' not in st.session_state:
            with st.spinner("Sinkronisasi harga market..."):
                res = post_data({"action": "get_logbook", "username": st.session_state['username']})
                if res and res.get("status") == "success":
                    st.session_state['logbook_data'] = res.get("data", [])
                else:
                    st.error("Gagal memuat data portofolio.")
                    
        if 'logbook_data' in st.session_state:
            df_logbook = pd.DataFrame(st.session_state['logbook_data'])
            
            if not df_logbook.empty:
                df_logbook = df_logbook.drop(columns=['Username Pemilik', 'Status Email'], errors='ignore')
                
                try:
                    live_p = pd.to_numeric(df_logbook['Live Price'], errors='coerce').fillna(0)
                    entry_p = pd.to_numeric(df_logbook['Entry Price'], errors='coerce').fillna(0)
                    lot_vol = pd.to_numeric(df_logbook['Lot'], errors='coerce').fillna(0)
                    
                    df_logbook['Floating Profit'] = (live_p - entry_p) * lot_vol * 100
                    total_floating = df_logbook['Floating Profit'].sum()
                    df_logbook['Floating Profit'] = df_logbook['Floating Profit'].apply(format_rupiah)
                except Exception as e:
                    df_logbook['Floating Profit'] = "Rp 0"
                    total_floating = 0

                # --- PANGGIL FUNGSI CLEAN FORMAT DI SINI ---
                df_logbook = clean_dataframe_format(df_logbook)

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("📌 Emiten Aktif", len(df_logbook))
                m2.metric("⏳ Status HOLD", len(df_logbook[df_logbook['Status'].astype(str).str.contains("HOLD|RISK", case=False, na=False)]))
                m3.metric("🚀 Kena TP", len(df_logbook[df_logbook['Status'].astype(str).str.contains("TP", case=False, na=False)]))
                m4.metric("💸 Total Unrealized PnL", format_rupiah(total_floating), delta=f"{total_floating:,.0f}" if total_floating != 0 else None)
                
                st.markdown("---")
                f1, f2 = st.columns(2)
                with f1:
                    search_query = st.text_input("🔍 Cari Kode Emiten", "")
                with f2:
                    status_filter = st.selectbox("📂 Filter Status", ["Semua", "HOLD", "TP", "CUTLOSS", "RISK-FREE"])
                    
                if search_query:
                    df_logbook = df_logbook[df_logbook['Emiten'].astype(str).str.contains(search_query.upper(), na=False)]
                if status_filter != "Semua":
                    df_logbook = df_logbook[df_logbook['Status'].astype(str).str.contains(status_filter, case=False, na=False)]
                
                cols = df_logbook.columns.tolist()
                if 'Floating Profit' in cols:
                    cols.remove('Floating Profit')
                    try:
                        status_idx = cols.index('Status')
                        cols.insert(status_idx + 1, 'Floating Profit')
                    except:
                        cols.append('Floating Profit')
                    df_logbook = df_logbook[cols]

                st.dataframe(style_dataframe(df_logbook), width='stretch', hide_index=True, height=400)
                
                st.markdown("---")
                with st.expander("⚙️ Action Menu: Realisasi Profit / Cutloss / Hapus Kesalahan Input"):
                    emiten_list = df_logbook['Emiten'].tolist()
                    if emiten_list:
                        action_col, emiten_col = st.columns(2)
                        with action_col:
                            pilihan_aksi = st.radio("Pilih Eksekusi:", ["✅ Realisasikan (Pindah ke Histori)", "🗑️ Hapus Permanen"])
                        with emiten_col:
                            target_emiten = st.selectbox("Pilih Saham:", emiten_list)
                        
                        if st.button("⚡ Jalankan Eksekusi", width='stretch'):
                            action_type = "move_to_history" if "Histori" in pilihan_aksi else "delete_logbook"
                            with st.spinner("Memproses ke pangkalan data..."):
                                res_action = post_data({
                                    "action": action_type, 
                                    "username": st.session_state['username'], 
                                    "emiten": target_emiten
                                })
                                if res_action and res_action.get("status") == "success":
                                    st.success(f"{target_emiten} berhasil diproses!")
                                    st.session_state.pop('logbook_data', None)
                                    st.rerun()
                                else:
                                    st.error("Gagal memproses data.")
            else:
                st.info("📂 Portofolio Anda masih kosong. Silakan analisa saham pertama Anda!")
                
    with tab_hist:
        st.markdown("### 🏆 Kalkulator Akurasi & Histori Jurnal")
        if st.button("📥 Muat Riwayat Trading", width='stretch'):
            with st.spinner("Menggali brankas histori..."):
                res_hist = post_data({"action": "get_history", "username": st.session_state['username']})
                if res_hist and res_hist.get("status") == "success":
                    st.session_state['history_data'] = res_hist.get("data", [])
                else:
                    st.error("Gagal menarik riwayat.")
                    
        if 'history_data' in st.session_state:
            df_hist = pd.DataFrame(st.session_state['history_data'])
            if not df_hist.empty:
                df_hist = df_hist.drop(columns=['Username Pemilik', 'Status Email'], errors='ignore')
                
                # --- PANGGIL FUNGSI CLEAN FORMAT DI HISTORI ---
                df_hist = clean_dataframe_format(df_hist)
                
                total_trade = len(df_hist)
                win_trade = len(df_hist[df_hist['Status'].astype(str).str.contains("TP", case=False, na=False)])
                loss_trade = len(df_hist[df_hist['Status'].astype(str).str.contains("CUTLOSS", case=False, na=False)])
                
                win_rate = (win_trade / total_trade) * 100 if total_trade > 0 else 0
                
                w1, w2, w3, w4 = st.columns(4)
                w1.metric("⚔️ Total Trade", total_trade)
                w2.metric("🟢 Win (Profit)", win_trade)
                w3.metric("🔴 Loss (Rugi)", loss_trade)
                w4.metric("📈 Akurasi (Win-Rate)", f"{win_rate:.1f}%")
                
                st.dataframe(style_dataframe(df_hist), width='stretch', hide_index=True, height=400)
            else:
                st.info("Riwayat trading Anda masih kosong.")
