import streamlit as st
import json
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="WRC Garage Admin", page_icon="📝", layout="wide")

# --- NAMA FILE DATABASE ---
# Data akan disimpan di file ini, bukan di dalam kodingan python lagi
DB_FILE = 'wrc_db.json'

# --- DATA AWAL (DEFAULT) ---
# Jika file JSON belum ada, kita pakai data ini sebagai permulaan
default_data = {
    "Mitsubishi Lancer Evolution VI GSR": {
        "images": ["https://raw.githubusercontent.com/USER/REPO/main/images/evo6.avif"], # Ganti link dummy
        "tahun": "1999",
        "specs": "4G63 2.0L Turbo",
        "driver": "Tommi Mäkinen 🇫🇮"
    }
}

# --- FUNGSI SERVER (LOAD & SAVE) ---
def load_data():
    """Membaca data dari file JSON"""
    if not os.path.exists(DB_FILE):
        return default_data
    
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default_data

def save_data(new_data):
    """Menulis/Menyimpan data ke file JSON"""
    with open(DB_FILE, 'w') as f:
        json.dump(new_data, f, indent=4)

# --- LOAD DATA SAAT APLIKASI DIMULAI ---
gallery_data = load_data()

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("🔧 Menu Server")
menu = st.sidebar.radio("Pilih Mode:", ["Galeri (Lihat Data)", "Input Data Baru"])

# =========================================
# MODE 1: INPUT DATA BARU (ADMIN)
# =========================================
if menu == "Input Data Baru":
    st.title("📝 Tambah Mobil Baru")
    st.markdown("Masukkan data mobil WRC baru di sini. Data akan disimpan ke server.")

    with st.form("form_tambah_mobil", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name_input = st.text_input("Nama Mobil (Cth: Subaru Impreza)")
            year_input = st.text_input("Tahun")
            driver_input = st.text_input("Driver")
        
        with col2:
            specs_input = st.text_area("Spesifikasi Mesin")
            # User harus memasukkan Link Gambar (URL) karena upload file fisik ke GitHub via Streamlit itu rumit
            img_url_input = st.text_input("URL Gambar (Link Internet/GitHub Raw)")
            
        submitted = st.form_submit_button("💾 Simpan ke Database")

        if submitted:
            if name_input and img_url_input:
                # 1. Siapkan struktur data baru
                new_entry = {
                    "images": [img_url_input], # Kita buat list agar format sama
                    "tahun": year_input,
                    "specs": specs_input,
                    "driver": driver_input
                }
                
                # 2. Masukkan ke dictionary utama
                gallery_data[name_input] = new_entry
                
                # 3. Panggil fungsi SAVE
                save_data(gallery_data)
                
                st.success(f"Berhasil! {name_input} telah disimpan ke database.")
                st.balloons()
            else:
                st.error("Nama Mobil dan URL Gambar wajib diisi!")

# =========================================
# MODE 2: GALERI (VIEWER)
# =========================================
elif menu == "Galeri (Lihat Data)":
    st.title("🏎️ WRC Garage Gallery")
    
    if not gallery_data:
        st.warning("Database kosong.")
    else:
        # Pilihan Mobil
        selected_car = st.selectbox("Pilih Mobil:", list(gallery_data.keys()))
        
        # Tampilkan Data
        car_info = gallery_data[selected_car]
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.info(f"📅 **Tahun:** {car_info.get('tahun', '-')}")
        c2.warning(f"⚙️ **Specs:** {car_info.get('specs', '-')}")
        c3.success(f"👤 **Driver:** {car_info.get('driver', '-')}")
        
        st.markdown("### Foto")
        # Logic gambar (bisa handle list gambar atau string tunggal)
        imgs = car_info.get('images', [])
        if isinstance(imgs, str): imgs = [imgs] # Jaga-jaga kalau formatnya string
        
        cols = st.columns(3)
        for i, img_url in enumerate(imgs):
            with cols[i % 3]:
                st.image(img_url, use_container_width=True)
