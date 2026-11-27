import streamlit as st
import pandas as pd
import gspread

st.header("2. Statistik & Produk Terlaris")

try:
    client = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
    sheet = client.open("Rekap_Pesanan_Toko").sheet1
    records = sheet.get_all_records()
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    st.stop()

if not records:
    st.info("Belum ada data penjualan untuk dianalisis.")
    st.stop()

df = pd.DataFrame(records)
df["Harga"] = pd.to_numeric(df["Harga"], errors="coerce").fillna(0)
df["Qty"] = pd.to_numeric(df.get("Qty", 1), errors="coerce").fillna(1)
df["Tanggal"] = pd.to_datetime(df["Waktu"], errors="coerce")
df["Bulan"] = df["Tanggal"].dt.strftime("%Y-%m").fillna("Tanpa Tanggal")

daftar_bulan = sorted(df["Bulan"].unique(), reverse=True)
pilih_bulan = st.selectbox("Pilih Periode Bulan (Tahun-Bulan):", daftar_bulan)
df_bulan = df[df["Bulan"] == pilih_bulan]

c1, c2, c3 = st.columns(3)
c1.metric("Total Omzet Bulan Ini", f"Rp {df_bulan['Harga'].sum():,.0f}")
c2.metric("Total Terjual", f"{int(df_bulan['Qty'].sum())} Item / Porsi")
lunas = df_bulan[df_bulan["Status"] == "Lunas"]["Harga"].sum()
c3.metric("Sudah Lunas", f"Rp {lunas:,.0f}")

st.divider()

st.subheader(f"Peringkat Produk Paling Laku ({pilih_bulan})")
if "Pesanan" in df_bulan.columns:
    rekap_produk = (
        df_bulan.groupby("Pesanan", as_index=False)
        .agg(
            Total_Terjual=("Qty", "sum"),
            Jumlah_Transaksi=("Pesanan", "count"),
            Total_Omzet=("Harga", "sum")
        )
        .sort_values(by="Total_Terjual", ascending=False)
    )
    st.bar_chart(rekap_produk.set_index("Pesanan")["Total_Terjual"])
    st.dataframe(rekap_produk, use_container_width=True, hide_index=True)
