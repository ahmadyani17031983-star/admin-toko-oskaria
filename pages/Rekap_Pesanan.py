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

def simpan_ke_sheet(data_dict):
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
        alamat = st.text_area("Alamat Kirim", height=70)
        pesanan = st.text_area("Detail Pesanan", height=80)
        ucapan = st.text_input("Kartu Ucapan (opsional)")
        kirim = st.text_input("Waktu Kirim (contoh: Besok jam 10)")
        harga_m = st.number_input("Total Harga (Rp)", min_value=0, step=5000, key="h_manual")
        status_m = st.selectbox("Status Bayar", ["Belum Bayar", "DP", "Lunas"], key="s_manual")

        if st.button("Simpan Pesanan", type="primary", key="btn_manual"):
            if pemesan.strip() or pesanan.strip():
                simpan_ke_sheet({
                    "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Pemesan": pemesan.strip(),
                    "HP": f"'{hp.strip()}" if hp.strip() else "",
                    "Alamat": alamat.strip(),
                    "Pesanan": pesanan.strip(),
                    "Ucapan": ucapan.strip(),
                    "Kirim": kirim.strip(),
                    "Harga": harga_m,
                    "Status": status_m
                })
            else:
                st.warning("Isi minimal Nama Pemesan atau Detail Pesanan.")

    with tab_wa:
        teks_wa = st.text_area(
            "Tempel (Paste) Format Order WA:",
            height=180,
            placeholder="- Nama Pemesan: Ibu Rina\n- No HP Penerima: 08123456789\n- Alamat: Jl. Poros Rappang\n- Pesanan: Parcel Buah + Puding\n- Kartu Ucapan: Cepat sembuh\n- Waktu Kirim: Besok jam 10"
        )
        harga_w = st.number_input("Total Harga (Rp)", min_value=0, step=5000, key="h_wa")
        status_w = st.selectbox("Status Bayar", ["Belum Bayar", "DP", "Lunas"], key="s_wa")

        if st.button("Simpan Pesanan", type="primary", key="btn_wa") and teks_wa.strip():
            data = {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Pemesan": "", "HP": "", "Alamat": "",
                "Pesanan": "", "Ucapan": "", "Kirim": "",
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
                    elif "ucapan" in k: data["Ucapan"] = v
                    elif "waktu" in k: data["Kirim"] = v
            simpan_ke_sheet(data)

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
