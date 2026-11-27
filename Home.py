import streamlit as st

st.set_page_config(page_title="Admin Toko Buah & Kue", layout="wide")
st.title("Admin Jualan: Puding, Buah Segar & Kue")
st.write("Silakan pilih menu di pojok kiri atas (tanda panah `>`) untuk mulai mengelola toko:")

st.info("""
1. **Rekap WA:** Tempel pesanan dari WhatsApp, otomatis tersimpan ke Google Sheets & hitung omzet.
2. **Foto Katalog:** Tambah nama toko, label harga, dan keterangan pada foto produk.
3. **Caption IG:** Buat teks promosi dan tagar lokal otomatis siap salin ke Instagram.
""")
