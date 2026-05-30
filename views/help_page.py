import streamlit as st

def render():
    st.markdown("## 📘 PANDUAN PENGGUNAAN BANDARLOGI TERMINAL")
    st.info("Selamat datang di **BandarLogi Terminal!** Ini adalah dasbor trading cerdas yang akan membantu Anda menganalisis pergerakan bandar, merancang trading plan otomatis, hingga memantau Live Portofolio Anda dalam satu tempat.")
    
    st.markdown("### Ikuti 5 langkah mudah berikut untuk memulai perjalanan trading Anda:")
    
    with st.expander("🔑 Langkah 1: Akses Masuk & Pendaftaran Akun", expanded=True):
        st.markdown("""
        1. Buka halaman aplikasi BandarLogi.
        2. Jika Anda belum memiliki akun, klik tab **"📝 Daftar Baru"**. Isi Username, Email aktif, dan Password. Lalu klik Daftar Sekarang.
        3. Jika sudah punya akun, masuk melalui tab **"🔑 Masuk"**.
        
        *(Tips: Jika lupa password, gunakan tab "🆘 Reset Password", sistem akan mengirimkan password ke email Anda secara otomatis).*
        """)

    with st.expander("⚡ Langkah 2: Melakukan Analisis Saham", expanded=True):
        st.markdown("""
        Setelah masuk, Anda akan berada di menu utama. Di menu sebelah kiri, pilih **"⚡ Terminal Analisis"**.
        1. Klik menu dropdown **"📝 Form Input Data Bandarmologi"** untuk membuka form.
        2. Masukkan Kode Emiten saham yang ingin dianalisis (Contoh: BBCA atau GOTO).
        3. Masukkan Total Net Buy satu bulan terakhir (dalam miliar).
        4. Masukkan **Top 5 Buyers** (Broker yang paling banyak membeli) dan **Top 5 Sellers** (Broker yang paling banyak menjual) dalam 1 bulan tarakhir. *(Data ini bisa Anda lihat dari menu 'Broker Summary' di aplikasi sekuritas Anda masing-masing).*
        5. Klik tombol **"🚀 Eksekusi Algoritma"**.
        
        **Sistem akan langsung memunculkan Trading Intelligence yang berisi:**
        * **Grade & Skor:** Seberapa kuat akumulasi bandar pada saham tersebut.
        * **Trading Plan:** Angka pasti untuk harga beli (Entry Price), Target Profit (TP 1, TP 2, TP 3), dan batas kerugian (Cutloss).
        * **Grafik Interaktif:** Grafik Candlestick pergerakan saham selama 3 bulan terakhir.
        """)

    with st.expander("💼 Langkah 3: Eksekusi & Simpan ke Portofolio", expanded=True):
        st.markdown("""
        Jika Anda merasa Trading Plan dari langkah 2 menarik dan Anda memutuskan untuk membeli saham tersebut:
        1. Scroll ke bawah dan buka menu **"💼 Eksekusi & Simpan ke Portofolio"**.
        2. Tentukan Tanggal Transaksi.
        3. Masukkan Volume (Jumlah Lot) yang Anda beli.
        4. Klik **"Amankan ke Jurnal Trading"**.
        
        *Plan tersebut kini resmi masuk ke dalam pantauan Live Portofolio Anda!*
        """)

    with st.expander("💸 Langkah 4: Memantau Live Portofolio (Uang Berjalan)", expanded=True):
        st.markdown("""
        Pindah ke menu sebelah kiri, pilih **"🎯 Portofolio & Jurnal"**. Anda akan berada di tab **"💼 Live Portofolio"**.
        1. **Tombol Sync Market:** Selalu klik tombol **"🔄 Sync Market"** untuk menarik harga saham terbaru secara real-time.
        2. **Cek Floating Profit:** Perhatikan kolom Floating Profit di tabel. Jika angkanya hijau (contoh: + Rp 150.000), artinya Anda sedang untung. Jika merah, Anda sedang rugi.
        3. **Pantau Indikator Status:**
           * ⏳ **HOLD:** Harga masih bergerak di area beli, tahan saham Anda.
           * 🛡️ **RISK-FREE:** Harga sudah naik melewati TP 1. Posisi Anda sudah aman!
           * ✅ **HIT!:** Target TP atau Cutloss sudah tersentuh.
        4. **Auto-Save Tanggal:** Saat status berubah menjadi "HIT", kolom Tanggal Hit akan otomatis mencatat dan mengunci tanggal hari itu sebagai dokumentasi Anda.
        """)

    with st.expander("🏆 Langkah 5: Realisasi Profit & Evaluasi Win-Rate", expanded=True):
        st.markdown("""
        Jika sebuah saham sudah mencapai Target (TP) atau Cutloss, dan Anda sudah menjualnya di aplikasi sekuritas, saatnya merealisasikan data tersebut:
        1. Di halaman Portofolio, scroll ke bawah dan buka menu **"⚙️ Action Menu"**.
        2. Pilih saham yang sudah dijual, lalu pilih aksi **"✅ Realisasikan (Pindah ke Histori)"**. Klik tombol Eksekusi.
           *(Saham tersebut akan hilang dari portofolio aktif dan masuk ke brankas histori).*
        3. **Cek Akurasi Trading:** Buka tab **"🏆 Histori & Win-Rate"** di bagian atas. Klik **"📥 Muat Riwayat Trading"**. Di sini Anda bisa melihat rasio kemenangan (Win-Rate), total profit, dan total kerugian dari seluruh sejarah trading Anda.
        """)

    st.markdown("---")
    st.markdown("### 💡 Tips Tambahan:")
    st.info("""
    * Anda dapat mencari saham spesifik atau memfilter saham yang berstatus "HOLD" saja menggunakan fitur pencarian di atas tabel portofolio.
    * Data Anda 100% aman dan terenkripsi. Pengguna lain tidak bisa melihat isi portofolio Anda.
    
    **Selamat Trading & Salam Cuan! 🚀💎**
    """)
