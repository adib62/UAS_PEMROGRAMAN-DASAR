import streamlit as st
import requests  # <--- Library buat nelfon Server

# 1. Konfigurasi Halaman
st.set_page_config(layout="centered", page_title="WRC Gallery Client", page_icon="🏎️")

# --- CSS ---
st.markdown("""
<style>
    .stButton button {width: 100%; border-radius: 20px;}
    div[data-testid="stImage"] img {border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
    .info-box { background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #4e4e4e; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI REQUEST KE SERVER ---
def get_data_from_server():
    """Fungsi ini bertugas mengambil data dari Server FastAPI"""
    try:
        # Menghubungi Server di port 8000
        response = requests.get("http://127.0.0.1:8000/api/wrc_data")
        
        # Kalau server bilang OK (200), ambil datanya
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Gagal koneksi ke server.")
            return {}
    except:
        st.error("🚨 Server Mati! Jalankan 'server_wrc.py' dulu di terminal lain.")
        return {}

# --- PANGGIL DATA ---
# Client tidak punya data sendiri, dia minta ke server
gallery_data = get_data_from_server()

# Kalau data kosong (server belum nyala), hentikan aplikasi
if not gallery_data:
    st.stop()

# --- LOGIKA UI (SAMA SEPERTI SEBELUMNYA) ---
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = list(gallery_data.keys())[0]
if 'img_index' not in st.session_state:
    st.session_state.img_index = 0

st.title("WRC Interactive Gallery")
st.caption("Mode: Client-Server Architecture")

pilihan_mobil = st.selectbox("Pilih Mobil:", list(gallery_data.keys()))

if pilihan_mobil != st.session_state.selected_car:
    st.session_state.selected_car = pilihan_mobil
    st.session_state.img_index = 0

st.divider()

@st.fragment
def show_gallery_interactive():
    data_mobil = gallery_data[st.session_state.selected_car]
    list_gambar = data_mobil["images"]
    jumlah_gambar = len(list_gambar)
    
    if st.session_state.img_index >= jumlah_gambar:
        st.session_state.img_index = 0

    current_url = list_gambar[st.session_state.img_index]
    st.image(current_url, caption=f"images {st.session_state.img_index + 1} dari {jumlah_gambar}", use_container_width=True)
    
    col_kiri, col_tengah, col_kanan = st.columns([1, 2, 1])
    
    with col_kiri:
        if st.button("⬅️ Sebelumnya"):
            st.session_state.img_index = (st.session_state.img_index - 1) % jumlah_gambar
            st.rerun()
            
    with col_kanan:
        if st.button("Berikutnya ➡️"):
            st.session_state.img_index = (st.session_state.img_index + 1) % jumlah_gambar
            st.rerun()

    with col_tengah:
        st.progress((st.session_state.img_index + 1) / jumlah_gambar)

    with st.container():
        st.markdown(f"### {st.session_state.selected_car}")
        k1, k2 = st.columns(2)
        with k1:
            st.write(f"**📅 Tahun:** {data_mobil['tahun']}")
            st.write(f"**👤 Driver:** {data_mobil['driver']}")
        with k2:
            st.write(f"**⚙️ Specs:** {data_mobil['specs']}")

show_gallery_interactive()
st.divider()