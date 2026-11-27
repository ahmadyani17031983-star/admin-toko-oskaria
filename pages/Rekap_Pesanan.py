import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.header("1. Rekap Pesanan WA ke Google Sheets")

scopes = [
    "https://googleapis.com",
    "https://googleapis.com",
]

try:
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open("Rekap_Pesanan_Toko").sheet1
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets. Pastikan Secrets & nama file sudah benar. Detail: {e}")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    teks_wa = st.text_area(
        "Tempel (Paste) Format Order WA:",
        height=200,
        placeholder="- Nama Pemesan: Ibu Rina\n- No HP Penerima: 08123456789\n- Alamat: Jl. Poros Rappang\n- Pesanan: Parcel Buah + Puding\n- Kartu Ucapan: Cepat sembuh\n- Waktu Kirim: Besok jam 10"
    )
    harga = st.number_input("Total Harga (Rp)", min_value=0, step=5000)
    status = st.selectbox("Status Bayar", ["Belum Bayar", "DP", "Lunas"])

    if st.button("Simpan Pesanan", type="primary") and teks_wa.strip():
        data = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Pemesan": "", "HP": "", "Alamat": "",
            "Pesanan": "", "Ucapan": "", "Kirim": "",
            "Harga": harga, "Status": status
        }
        for b in teks_wa.strip().split("\n"):
            if ":" in b:
                k, v = b.split(":", 1)
                k, v = k.lower(), v.strip()
                if "pemesan" in k: data["Pemesan"] = v
                elif "hp" in k or "penerima" in k: data["HP"] = f"'{v}"
                elif "alamat" in k: data["Alamat"] = v
                elif "pesanan" in k: data["Pesanan"] = v
                elif "ucapan" in k: data["Ucapan"] = v
                elif "waktu" in k: data["Kirim"] = v

        if not sheet.row_values(1):
            sheet.append_row(list(data.keys()))

        sheet.append_row(list(data.values()), value_input_option="USER_ENTERED")
        st.success("Berhasil! Pesanan sudah tersimpan di Google Sheets.")
        st.rerun()

with col2:
    st.subheader("Ringkasan & Daftar Pesanan")
    records = sheet.get_all_records()
    if records:
        df = pd.DataFrame(records)
        df["Harga"] = pd.to_numeric(df["Harga"], errors="coerce").fillna(0)
        
        st.metric("Total Omzet Tercatat", f"Rp {df['Harga'].sum():,.0f}")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data pesanan di Google Sheets.")
