import streamlit as st
import requests  # Library wajib buat Client-Server

# ==========================================
# 1. KONFIGURASI HALAMAN & TAMPILAN
# ==========================================
st.set_page_config(
    page_title="WRC Garage Client",
    page_icon="🏎️",
    layout="centered"
)

# Custom CSS biar tampilan makin sangar
st.markdown("""
<style>
    /* Bikin tombol jadi bulat dan full width */
    .stButton button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
    }
    
    /* Kasih bayangan di gambar biar pop-up */
    div[data-testid="stImage"] img {
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        border: 2px solid #333;
    }

    /* Kotak Info Spesifikasi */
    .info-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ff4b4b;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIKA CLIENT (REQUEST DATA)
# ==========================================
def fetch_data_from_server():
    """
    Fungsi ini bertugas 'menelpon' Server FastAPI
    untuk meminta data mobil terbaru.
    """
    api_url = "http://127.0.0.1:8000/api/wrc_data"
    
    try:
        response = requests.get(api_url)
        
        # Cek apakah server mengangkat telpon (Status 200 OK)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"⚠️ Server error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("🚨 **KONEKSI GAGAL!** Server belum dinyalakan.")
        st.info("💡 **Solusi:** Buka terminal baru, ketik `uvicorn server_wrc:app --reload`")
        return None

# --- EKSEKUSI PENGAMBILAN DATA ---
gallery_data = fetch_data_from_server()

# Jika data kosong (server mati), stop aplikasi biar gak error
if not gallery_data:
    st.stop()

# ==========================================
# 3. STATE MANAGEMENT (INGATAN APLIKASI)
# ==========================================
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = list(gallery_data.keys())[0]

if 'img_index' not in st.session_state:
    st.session_state.img_index = 0

# ==========================================
# 4. UI: HEADER & PILIHAN MOBIL
# ==========================================
st.title("🏎️ WRC Interactive Garage")
st.markdown("Aplikasi **Client-Side** yang mengambil data real-time dari Server FastAPI.")
st.divider()

# Dropdown Pilihan Mobil
pilihan_mobil = st.selectbox(
    "📂 Pilih Koleksi Mobil:", 
    list(gallery_data.keys())
)

# Logic: Kalau ganti mobil, reset gambar ke nomor 1
if pilihan_mobil != st.session_state.selected_car:
    st.session_state.selected_car = pilihan_mobil
    st.session_state.img_index = 0

st.write("") # Spasi kosong dikit

# ==========================================
# 5. UI: GALERI INTERAKTIF (FRAGMENT)
# ==========================================
@st.fragment
def show_gallery_interactive():
    # A. Ambil Data
