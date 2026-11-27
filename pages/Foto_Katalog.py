import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.header("2. Buat Foto Katalog IG & Status WA")
foto = st.file_uploader("Unggah Foto Produk (JPG/PNG)", type=["jpg", "jpeg", "png"])

if foto:
    c1, c2 = st.columns(2)
    with c1:
        toko = st.text_input("Nama Toko", "@NamaTokoIstri")
        produk = st.text_input("Nama Produk", "Parcel Buah Segar")
        harga = st.text_input("Harga", "Rp 250.000")
        info = st.text_input("Keterangan", "Ready Stock • Free Kartu Ucapan")
    with c2:
        img = Image.open(foto).convert("RGBA")
        h_new = int(img.size[1] * (1080 / img.size[0]))
        img = img.resize((1080, h_new))
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.rectangle([(0, h_new - 210), (1080, h_new)], fill=(20, 20, 20, 195))
        d.rectangle([(710, h_new - 175), (1040, h_new - 90)], fill=(220, 53, 69, 255))
        f_lg, f_md = ImageFont.load_default(size=40), ImageFont.load_default(size=26)
        d.text((40, h_new - 180), produk, fill=(255, 255, 255, 255), font=f_lg)
        d.text((40, h_new - 120), info, fill=(220, 220, 220, 255), font=f_md)
        d.text((40, h_new - 70), f"Order WA/IG: {toko}", fill=(255, 215, 0, 255), font=f_md)
        d.text((735, h_new - 155), harga, fill=(255, 255, 255, 255), font=f_lg)

        hasil = Image.alpha_composite(img, ov).convert("RGB")
        st.image(hasil, use_container_width=True)
        buf = io.BytesIO()
        hasil.save(buf, format="JPEG", quality=90)
        st.download_button("Download Foto Katalog", buf.getvalue(), "katalog.jpg", "image/jpeg", type="primary")
