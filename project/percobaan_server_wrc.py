import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="WRC Rally Garage",
    page_icon="🚗",
    layout="wide"
)

# --- DATABASE (Tetap disimpan di dalam script) ---
gallery_data = {
    "Mitsubishi Lancer Evolution VI GSR": {
        "images": [
            "project/images/Mitsubishi Lancer Evolution VI GSR View_A.avif", "images/Mitsubishi Lancer Evolution VI GSR View_B.avif", 
            "images/Mitsubishi Lancer Evolution VI GSR View_C.avif", "images/Mitsubishi Lancer Evolution VI GSR View_D.avif"
        ],
        "tahun": "1999 (Special Edition)",
        "specs": "4G63 2.0L Turbo, 280 PS / 373 Nm, AWD 5-Speed",
        "driver": "Tommi Mäkinen 🇫🇮"
    },
    "Audi Quattro S1 E2": {
        "images": [
            "images/Audi Quattro S1 E2 View_A.avif", "images/Audi Quattro S1 E2 View_B.avif"
        ],
        "tahun": "1985 (Group B)",
        "specs": "2.1L I5 Turbo, 591 HP, Quattro AWD",
        "driver": "Walter Röhrl 🇩🇪 / Stig Blomqvist 🇸🇪"
    },
    "Lancia Delta HF Integrale": {
        "images": [
            "images/Lancia Delta HF Integrale View_A.avif", "images/Lancia Delta HF Integrale View_B.avif"
        ],
        "tahun": "1992 (Evo)",
        "specs": "2.0L Turbo 16V, 210 HP, 4WD",
        "driver": "Juha Kankkunen 🇫🇮 / Miki Biasion 🇮🇹"
    },
    "Mitsubishi Lancer Evolution V GSR": {
        "images": [
            "images/Mitsubishi Lancer Evolution V GSR View_A.avif", "images/Mitsubishi Lancer Evolution V GSR View_B.avif"
        ],
        "tahun": "1998",
        "specs": "4G63 Turbo, 276 HP, AWD",
        "driver": "Tommi Mäkinen 🇫🇮"
    },
    "Mitsubishi Lancer Evolution X": {
        "images": [
            "images/Mitsubishi Lancer Evolution X View_A.avif", "images/Mitsubishi Lancer Evolution X View_B.avif"
        ],
        "tahun": "2007 - 2016",
        "specs": "4B11T 2.0L Turbo, 291 HP, S-AWC",
        "driver": "Fumio Nutahara 🇯🇵"
    },
    "Mitsubishi Lancer Evolution X Kaela Kovalskia": {
        "images": [
            "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_A.avif", 
            "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_B.avif"
        ],
        "tahun": "2023 (Hololive Edition)",
        "specs": "Custom Tuned 4B11T, 400+ HP",
        "driver": "Kaela Kovalskia 🔨"
    },
    "Subaru Impreza 1995 555": {
        "images": [
            "images/Subaru Impreza 1995 555 View_A.avif", "images/Subaru Impreza 1995 555 View_B.avif"
        ],
        "tahun": "1995 (Group A)",
        "specs": "Ej20 Boxer Turbo, 300 HP, AWD",
        "driver": "Colin McRae 🏴󠁧󠁢󠁳󠁣󠁴󠁿"
    },
    "Subaru WRX STi NR4": {
        "images": [
            "images/Subaru WRX STi NR4 View_A.avif", "images/Subaru WRX STi NR4 View_B.avif"
        ],
        "tahun": "2015 (Production Cup)",
        "specs": "2.0L Boxer Turbo, 280 HP, AWD",
        "driver": "Mark Higgins 🇬🇧"
    }
}

# --- SIDEBAR (Navigasi / Pilihan) ---
st.sidebar.title("🏁 WRC Garage")
st.sidebar.write("Pilih mobil legendaris di bawah ini:")

# Membuat dropdown dari key dictionary
selected_car_name = st.sidebar.selectbox(
    "Daftar Mobil",
    options=list(gallery_data.keys())
)

# Ambil data berdasarkan pilihan
car_info = gallery_data[selected_car_name]

# --- MAIN PAGE (Tampilan Utama) ---
st.title(f"{selected_car_name}")
st.markdown("---")

# Tampilan Kolom untuk Spesifikasi
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"**Tahun:**\n{car_info['tahun']}")

with col2:
    st.warning(f"**Spesifikasi:**\n{car_info['specs']}")

with col3:
    st.success(f"**Driver:**\n{car_info['driver']}")

st.markdown("### 📸 Gallery")

# Tampilkan Gambar (Logic Grid)
# Note: Streamlit perlu akses file lokal. Pastikan folder 'images/' ada di sebelah file .py ini.
images_list = car_info['images']

if images_list:
    # Buat grid 4 kolom
    cols = st.columns(4)
    for index, image_path in enumerate(images_list):
        with cols[index % 4]:
            try:
                # Menampilkan gambar
                st.image(image_path, caption=f"View {index+1}", use_container_width=True)
            except Exception:
                # Fallback jika gambar tidak ditemukan di folder lokal
                st.error(f"File tidak ditemukan: {image_path}")
else:
    st.write("Tidak ada gambar tersedia.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Streamlit")
