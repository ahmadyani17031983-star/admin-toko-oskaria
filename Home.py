import streamlit as st

st.set_page_config(page_title="Admin Toko Oskaria", page_icon="🍰", layout="wide")

st.title("Admin Jualan: Puding, Buah Segar & Kue 🍰")
st.write("Silakan pilih menu di pojok kiri atas (tanda panah `>`) untuk mulai mengelola toko:")

st.info(
    """
    1. **Rekap Pesanan:** Catat pesanan manual atau tempel format WA, otomatis tersimpan ke Google Sheets.
    2. **Statistik Penjualan:** Pantau total omzet bulanan, status pembayaran, dan peringkat produk paling laku.
    """
)
