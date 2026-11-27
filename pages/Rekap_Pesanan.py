import streamlit as st
import pandas as pd
import gspread
from datetime import datetime

st.header("1. Rekap Pesanan ke Google Sheets")

try:
    client = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
    sheet = client.open("Rekap_Pesanan_Toko").sheet1
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets. Detail: {e}")
    st.stop()

# Ambil data lama untuk menyusun daftar produk otomatis
records = sheet.get_all_records()
df_existing = pd.DataFrame(records) if records else pd.DataFrame()

menu_bawaan = [
    "Puding Buah",
    "Puding Cokelat",
    "Parcel Buah",
    "Buah Potong Segar",
    "Kue Tart / Ulang Tahun",
    "Kue Basah / Kotak",
]

# Gabungkan menu bawaan dengan nama produk yang sudah pernah diinput di Google Sheets
produk_tersimpan = []
if not df_existing.empty and "Pesanan" in df_existing.columns:
    produk_tersimpan = [str(x).strip() for x in df_existing["Pesanan"].unique() if str(x).strip()]

daftar_produk = sorted(list(set(menu_bawaan + produk_tersimpan)))
daftar_produk.append("+ Tambah Produk Baru...")

def simpan_ke_sheet(data_dict):
    # Pastikan baris header lengkap jika sheet masih kosong
    if not sheet.row_values(1):
        sheet.append_row(list(data_dict.keys()))
    sheet.append_row(list(data_dict.values()), value_input_option="USER_ENTERED")
    st.success("Berhasil! Pesanan sudah tersimpan di Google Sheets.")
    st.rerun()

col1, col2 = st.columns(2)

with col1:
    tab_manual, tab_wa = st.tabs(["Isi Kotak Manual", "Tempel Format WA"])

    with tab_manual:
        pemesan = st.text_input("Nama Pemesan")
        hp = st.text_input("No HP Penerima")
        alamat = st.text_area("Alamat Kirim", height=65)

        pilihan_produk = st.selectbox("Pilih Produk", daftar_produk)
        if pilihan_produk == "+ Tambah Produk Baru...":
            nama_produk = st.text_input("Ketik Nama Produk Baru (otomatis tersimpan ke daftar)")
        else:
            nama_produk = pilihan_produk

        qty = st.number_input("Jumlah (Qty / Porsi / Box)", min_value=1, step=1, value=1)
        catatan = st.text_input("Catatan / Kartu Ucapan (opsional)")
        kirim = st.text_input("Waktu Kirim (contoh: Besok jam 10)")
        harga_m = st.number_input("Total Harga (Rp)", min_value=0, step=5000, key="h_manual")
        status_m = st.selectbox("Status Bayar", ["Belum Bayar", "DP", "Lunas"], key="s_manual")

        if st.button("Simpan Pesanan", type="primary", key="btn_manual"):
            if nama_produk.strip():
                simpan_ke_sheet({
                    "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Pemesan": pemesan.strip(),
                    "HP": f"'{hp.strip()}" if hp.strip() else "",
                    "Alamat": alamat.strip(),
                    "Pesanan": nama_produk.strip(),
                    "Qty": qty,
                    "Catatan": catatan.strip(),
                    "Kirim": kirim.strip(),
                    "Harga": harga_m,
                    "Status": status_m
                })
            else:
                st.warning("Silakan pilih atau ketik nama produk terlebih dahulu.")

    with tab_wa:
        teks_wa = st.text_area(
            "Tempel (Paste) Format Order WA:",
            height=170,
            placeholder="- Nama Pemesan: Ibu Rina\n- No HP Penerima: 08123456789\n- Alamat: Jl. Poros Rappang\n- Pesanan: Parcel Buah\n- Catatan: Cepat sembuh\n- Waktu Kirim: Besok jam 10"
        )
        qty_w = st.number_input("Jumlah (Qty)", min_value=1, step=1, value=1, key="q_wa")
        harga_w = st.number_input("Total Harga (Rp)", min_value=0, step=5000, key="h_wa")
        status_w = st.selectbox("Status Bayar", ["Belum Bayar", "DP", "Lunas"], key="s_wa")

        if st.button("Simpan Pesanan", type="primary", key="btn_wa") and teks_wa.strip():
            data = {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Pemesan": "", "HP": "", "Alamat": "",
                "Pesanan": "", "Qty": qty_w, "Catatan": "", "Kirim": "",
                "Harga": harga_w, "Status": status_w
            }
            for b in teks_wa.strip().split("\n"):
                if ":" in b:
                    k, v = b.split(":", 1)
                    k, v = k.lower(), v.strip()
                    if "pemesan" in k: data["Pemesan"] = v
                    elif "hp" in k or "penerima" in k: data["HP"] = f"'{v}"
                    elif "alamat" in k: data["Alamat"] = v
                    elif "pesanan" in k: data["Pesanan"] = v
                    elif "ucapan" in k or "catatan" in k: data["Catatan"] = v
                    elif "waktu" in k: data["Kirim"] = v
            simpan_ke_sheet(data)

with col2:
    st.subheader("Ringkasan & Daftar Pesanan")
    if not df_existing.empty:
        df_existing["Harga"] = pd.to_numeric(df_existing["Harga"], errors="coerce").fillna(0)
        st.metric("Total Omzet Tercatat", f"Rp {df_existing['Harga'].sum():,.0f}")
        st.dataframe(df_existing, use_container_width=True)
    else:
        st.info("Belum ada data pesanan di Google Sheets.")
