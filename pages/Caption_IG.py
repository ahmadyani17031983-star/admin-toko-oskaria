import streamlit as st
import random

st.header("3. Pembuat Caption & Tagar Instagram")

kategori = st.selectbox("Kategori Produk", [
    "Parcel Buah & Buah Hias",
    "Puding Segar",
    "Buah Segar Impor",
    "Kue Basah (PO)",
    "Kue Kering & Hampers"
])

menu = st.text_input("Nama Menu / Varian", "Parcel Buah Mix Apel & Anggur")
keunggulan = st.text_input("Keunggulan / Promo", "Buah fresh pilihan, gratis kartu ucapan")
kota = st.text_input("Kota / Area Kirim", "Sidrap")
wa = st.text_input("Nomor WhatsApp", "0812-3456-7890")
gaya = st.radio("Gaya Bahasa", ["Ramah & Hangat", "Singkat & Promo"], horizontal=True)

if st.button("Buat Caption Sekarang", type="primary"):
    kota_tag = kota.lower().replace(" ", "")

    pembuka = {
        "Parcel Buah & Buah Hias": [
            f"Mau jenguk kerabat atau kirim bingkisan spesial di area {kota}? 🎁🍎",
            f"Sampaikan perhatian manis lewat rangkaian {menu} yang rapi dan segar ✨"
        ],
        "Puding Segar": [
            f"Cuaca panas paling pas ditemani yang lembut dan dingin! 🍮✨",
            f"Cari dessert lembut untuk keluarga di {kota}? Cobain {menu} kami! 😋"
        ],
        "Buah Segar Impor": [
            f"Baru datang! Stok {menu} manis dan renyah siap masuk kulkas di rumah 🍇🍊",
            f"Jaga kesehatan keluarga dengan pilihan {menu} terbaik hari ini 🍎✨"
        ],
        "Kue Basah (PO)": [
            f"Butuh suguhan untuk arisan, pengajian, atau rapat di {kota}? 🥮☕",
            f"Fresh dari dapur! Open PO {menu} buatan rumahan tanpa pengawet 🌿"
        ],
        "Kue Kering & Hampers": [
            f"Teman ngeteh sore paling pas atau ide hampers cantik untuk orang tersayang 🍪🎁",
            f"Renyah dan wangi butter! {menu} siap menemani momen kumpul keluarga ✨"
        ]
    }

    tagar = {
        "Parcel Buah & Buah Hias": f"#parcelbuah{kota_tag} #buahhias{kota_tag} #hampersbuah{kota_tag} #parcelbuahsegar #parceljenguk",
        "Puding Segar": f"#puding{kota_tag} #dessert{kota_tag} #pudinghomemade #pudingbuah #kuliner{kota_tag}",
        "Buah Segar Impor": f"#buahsegar{kota_tag} #buahimpor{kota_tag} #tokobuah{kota_tag} #buahfresh",
        "Kue Basah (PO)": f"#kuebasah{kota_tag} #snackbox{kota_tag} #kuearisan #jajananpasar #kuliner{kota_tag}",
        "Kue Kering & Hampers": f"#kuekering{kota_tag} #hamperskue{kota_tag} #cookies{kota_tag} #topleskue #kuliner{kota_tag}"
    }

    awal = random.choice(pembuka[kategori])

    if gaya == "Ramah & Hangat":
        teks = (
            f"{awal}\n\n"
            f"✨ *{menu}*\n"
            f"✅ {keunggulan}\n"
            f"🚚 Siap antar area {kota} & sekitarnya\n\n"
            f"Yuk amankan pesananmu sekarang sebelum kehabisan! 😊\n"
            f"📲 Order via WhatsApp: {wa} (atau klik link di bio)\n\n"
            f".\n.\n"
            f"{tagar[kategori]} #umkm{kota_tag}"
        )
    else:
        teks = (
            f"READY / OPEN PO: {menu.upper()}! 🔥\n\n"
            f"• {keunggulan}\n"
            f"• Pengiriman area {kota}\n\n"
            f"Pesan cepat via WA: {wa} 📲\n\n"
            f"{tagar[kategori]} #kuliner{kota_tag}"
        )

    st.subheader("Hasil Caption Siap Salin:")
    st.code(teks, language=None)
