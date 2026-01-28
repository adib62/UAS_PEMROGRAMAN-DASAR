import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(layout="centered", page_title="WRC Auction House", page_icon="💰")

# Helper: Format Angka ke Rupiah (Titik tiap 3 digit)
def format_rupiah(nominal):
    return f"Rp {nominal:,.0f}".replace(",", ".")

# --- CSS TAMPILAN ---
st.markdown("""
<style>
    .stButton button {width: 100%; border-radius: 10px; font-weight: bold;}
    div[data-testid="stImage"] img {border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE LENGKAP (8 MOBIL)
# ==========================================
# Disimpan di session_state agar data tawaran tidak hilang saat ganti mobil
if 'gallery_data' not in st.session_state:
    st.session_state.gallery_data = {
        "Mitsubishi Lancer Evolution VI GSR": {
            "images": [f"images/Mitsubishi Lancer Evolution VI GSR View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "1999 (Special Edition)", "specs": "4G63 2.0L Turbo, 280 PS", "driver": "Tommi Mäkinen 🇫🇮",
            "price": 1500000000, "highest_bidder": "Belum ada"
        },
        "Audi Quattro S1 E2": {
            "images": [f"images/Audi Quattro S1 E2 View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "1985 (Group B)", "specs": "2.1L I5 Turbo, 591 HP", "driver": "Walter Röhrl 🇩🇪",
            "price": 5000000000, "highest_bidder": "Museum Jerman"
        },
        "Lancia Delta HF Integrale": {
            "images": [f"images/Lancia Delta HF Integrale View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "1992 (Evo)", "specs": "2.0L Turbo 16V, 210 HP", "driver": "Juha Kankkunen 🇫🇮",
            "price": 2800000000, "highest_bidder": "Kolektor Italia"
        },
        "Mitsubishi Lancer Evolution V GSR": {
            "images": [f"images/Mitsubishi Lancer Evolution V GSR View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "1998", "specs": "4G63 Turbo, 276 HP", "driver": "Tommi Mäkinen 🇫🇮",
            "price": 1200000000, "highest_bidder": "Belum ada"
        },
        "Mitsubishi Lancer Evolution X": {
            "images": [f"images/Mitsubishi Lancer Evolution X View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "2007 - 2016", "specs": "4B11T 2.0L Turbo, 291 HP", "driver": "Fumio Nutahara 🇯🇵",
            "price": 950000000, "highest_bidder": "Showroom JKT"
        },
        "Mitsubishi Lancer Evolution X Kaela Kovalskia": {
            "images": [f"images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "2023 (Hololive Edition)", "specs": "Custom Tuned 4B11T, 400+ HP", "driver": "Kaela Kovalskia 🔨",
            "price": 9999999999, "highest_bidder": "Simp No. 1"
        },
        "Subaru Impreza 1995 555": {
            "images": [f"images/Subaru Impreza 1995 555 View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "1995 (Group A)", "specs": "Ej20 Boxer Turbo, 300 HP", "driver": "Colin McRae 🏴󠁧󠁢󠁳󠁣󠁴󠁿",
            "price": 3500000000, "highest_bidder": "Colin McRae Fans"
        },
        "Subaru WRX STi NR4": {
            "images": [f"images/Subaru WRX STi NR4 View_{i}.avif" for i in ["A", "B", "C", "D", "E", "F", "G", "H"]],
            "tahun": "2015 (Production Cup)", "specs": "2.0L Boxer Turbo, 280 HP", "driver": "Mark Higgins 🇬🇧",
            "price": 1100000000, "highest_bidder": "Belum ada"
        }
    }

# Riwayat Tawaran
if 'bid_history' not in st.session_state:
    st.session_state.bid_history = []

# ==========================================
# 3. STATE MANAGEMENT & NAVIGASI
# ==========================================
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = list(st.session_state.gallery_data.keys())[0]
if 'img_index' not in st.session_state:
    st.session_state.img_index = 0

st.title("💰 WRC Championship Auction")
st.caption("Mode: All-in-One Standalone System")

pilihan_mobil = st.selectbox("📂 Pilih Unit Lelang:", list(st.session_state.gallery_data.keys()))

if pilihan_mobil != st.session_state.selected_car:
    st.session_state.selected_car = pilihan_mobil
    st.session_state.img_index = 0

st.divider()

# ==========================================
# 4. UI: GALERI & BIDDING
# ==========================================
@st.fragment
def show_auction_standalone():
    data_mobil = st.session_state.gallery_data[st.session_state.selected_car]
    list_gambar = data_mobil["images"]
    jumlah_gambar = len(list_gambar)
    
    # --- 📸 GALERI GAMBAR (NAVIGASI) ---
    current_path = list_gambar[st.session_state.img_index]
    
    # Safety Check: Pastikan file gambar ada
    if os.path.exists(current_path):
        st.image(current_path, caption=f"Lot: {st.session_state.selected_car}", use_container_width=True)
    else:
        st.error(f"⚠️ Gambar tidak ditemukan: `{current_path}`")
    
    col_prev, col_bar, col_next = st.columns([1, 4, 1], vertical_alignment="center")
    with col_prev:
        if st.button("◀️"):
            st.session_state.img_index = (st.session_state.img_index - 1) % jumlah_gambar
            st.rerun()
    with col_next:
        if st.button("▶️"):
            st.session_state.img_index = (st.session_state.img_index + 1) % jumlah_gambar
            st.rerun()
    with col_bar:
        st.progress((st.session_state.img_index + 1) / jumlah_gambar)
    
    # --- STATUS HARGA ---
    st.markdown("### 🔨 Status Lelang")
    c1, c2 = st.columns(2)
    c1.metric("Harga Tertinggi", format_rupiah(data_mobil['price']))
    c2.metric("Pemegang Bid", data_mobil['highest_bidder'])

    with st.expander("📄 Detail Spesifikasi"):
        st.write(f"**Tahun:** {data_mobil['tahun']}")
        st.write(f"**Driver:** {data_mobil['driver']}")
        st.write(f"**Specs:** {data_mobil['specs']}")

    # --- INPUT BIDDING (DENGAN TITIK OTOMATIS) ---
    st.markdown("### 💸 Masukkan Tawaran")
    with st.container(border=True):
        nama = st.text_input("Nama Anda:", placeholder="Contoh: Sultan Jogja")
        
        harga_input = st.number_input(
            "Nominal Tawaran (Rp):", 
            min_value=data_mobil['price'] + 1000000, 
            value=data_mobil['price'] + 10000000,
            step=10000000
        )
        
        # ✨ LIVE PREVIEW: Agar tidak bingung nominal
        st.info(f"Konfirmasi Angka: **{format_rupiah(harga_input)}**")
        
        if st.button("🔥 KIRIM BID SEKARANG", type="primary"):
            if not nama:
                st.warning("Nama wajib diisi!")
            elif harga_input <= data_mobil['price']:
                st.error("Tawaran harus lebih tinggi dari harga saat ini!")
            else:
                # Update Database Lokal
                st.session_state.gallery_data[st.session_state.selected_car]["price"] = harga_input
                st.session_state.gallery_data[st.session_state.selected_car]["highest_bidder"] = nama
                
                # Tambah ke Log Riwayat
                log = {
                    "Waktu": datetime.now().strftime("%H:%M:%S"),
                    "Mobil": st.session_state.selected_car,
                    "Penawar": nama,
                    "Nominal": format_rupiah(harga_input)
                }
                st.session_state.bid_history.insert(0, log)
                st.success(f"Tawaran {format_rupiah(harga_input)} diterima!")
                st.rerun()

show_auction_standalone()

# ==========================================
# 5. TABEL RIWAYAT
# ==========================================
st.divider()
st.subheader("📜 Log Riwayat Penawaran")
if st.session_state.bid_history:
    st.table(pd.DataFrame(st.session_state.bid_history))
else:
    st.info("Belum ada aktivitas lelang.")
