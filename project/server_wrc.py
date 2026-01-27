from fastapi import FastAPI
import uvicorn

app = FastAPI()

# --- DATABASE (Disimpan di Server) ---
# Client TIDAK BOLEH punya data ini. Client harus minta ke sini.
gallery_data = {
    "Mitsubishi Lancer Evolution VI GSR": {
        "images": [
            "images/Mitsubishi Lancer Evolution VI GSR View_A.avif", "images/Mitsubishi Lancer Evolution VI GSR View_B.avif", "images/Mitsubishi Lancer Evolution VI GSR View_C.avif",
            "images/Mitsubishi Lancer Evolution VI GSR View_D.avif", "images/Mitsubishi Lancer Evolution VI GSR View_E.avif", "images/Mitsubishi Lancer Evolution VI GSR View_F.avif",
            "images/Mitsubishi Lancer Evolution VI GSR View_G.avif", "images/Mitsubishi Lancer Evolution VI GSR View_H.avif"
        ],
        "tahun": "1999 (Special Edition)",
        "specs": "4G63 2.0L Turbo, 280 PS / 373 Nm, AWD 5-Speed",
        "driver": "Tommi Mäkinen 🇫🇮"
    },
    "Audi Quattro S1 E2": {
        "images": [
            "images/Audi Quattro S1 E2 View_A.avif", "images/Audi Quattro S1 E2 View_B.avif", "images/Audi Quattro S1 E2 View_C.avif",
            "images/Audi Quattro S1 E2 View_D.avif", "images/Audi Quattro S1 E2 View_E.avif", "images/Audi Quattro S1 E2 View_F.avif",
            "images/Audi Quattro S1 E2 View_G.avif", "images/Audi Quattro S1 E2 View_H.avif"
        ],
        "tahun": "1985 (Group B)",
        "specs": "2.1L I5 Turbo, 591 HP, Quattro AWD",
        "driver": "Walter Röhrl 🇩🇪 / Stig Blomqvist 🇸🇪"
    },
    "Lancia Delta HF Integrale": {
        "images": [
            "images/Lancia Delta HF Integrale View_A.avif", "images/Lancia Delta HF Integrale View_B.avif", "images/Lancia Delta HF Integrale View_C.avif",
            "images/Lancia Delta HF Integrale View_D.avif", "images/Lancia Delta HF Integrale view_E.avif", "images/Lancia Delta HF Integrale View_F.avif",
            "images/Lancia Delta HF Integrale View_G.avif", "images/Lancia Delta HF Integrale View_H.avif"
        ],
        "tahun": "1992 (Evo)",
        "specs": "2.0L Turbo 16V, 210 HP, 4WD",
        "driver": "Juha Kankkunen 🇫🇮 / Miki Biasion 🇮🇹"
    },
    "Mitsubishi Lancer Evolution V GSR": {
        "images": [
            "images/Mitsubishi Lancer Evolution V GSR View_A.avif", "images/Mitsubishi Lancer Evolution V GSR View_B.avif", "images/Mitsubishi Lancer Evolution V GSR View_C.avif",
            "images/Mitsubishi Lancer Evolution V GSR View_D.avif", "images/Mitsubishi Lancer Evolution V GSR View_E.avif", "images/Mitsubishi Lancer Evolution V GSR View_F.avif",
            "images/Mitsubishi Lancer Evolution V GSR View_G.avif", "images/Mitsubishi Lancer Evolution V GSR View_H.avif"
        ],
        "tahun": "1998",
        "specs": "4G63 Turbo, 276 HP, AWD",
        "driver": "Tommi Mäkinen 🇫🇮"
    },
    "Mitsubishi Lancer Evolution X": {
        "images": [
            "images/Mitsubishi Lancer Evolution X View_A.avif", "images/Mitsubishi Lancer Evolution X View_B.avif", "images/Mitsubishi Lancer Evolution X View_C.avif",
            "images/Mitsubishi Lancer Evolution X View_D.avif", "images/Mitsubishi Lancer Evolution X View_E.avif", "images/Mitsubishi Lancer Evolution X View_F.avif",
            "images/Mitsubishi Lancer Evolution X View_G.avif", "images/Mitsubishi Lancer Evolution X View_H.avif"
        ],
        "tahun": "2007 - 2016",
        "specs": "4B11T 2.0L Turbo, 291 HP, S-AWC",
        "driver": "Fumio Nutahara 🇯🇵"
    },
    "Mitsubishi Lancer Evolution X Kaela Kovalskia": {
        "images": [
            "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_A.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_B.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_C.avif",
            "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_D.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_E.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_F.avif",
            "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_G.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_H.avif"
        ],
        "tahun": "2023 (Hololive Edition)",
        "specs": "Custom Tuned 4B11T, 400+ HP",
        "driver": "Kaela Kovalskia 🔨"
    },
    "Subaru Impreza 1995 555": {
        "images": [
            "images/Subaru Impreza 1995 555 View_A.avif", "images/Subaru Impreza 1995 555 View_B.avif", "images/Subaru Impreza 1995 555 View_C.avif",
            "images/Subaru Impreza 1995 555 View_D.avif", "images/Subaru Impreza 1995 555 View_E.avif", "images/Subaru Impreza 1995 555 View_F.avif",
            "images/Subaru Impreza 1995 555 View_G.avif", "images/Subaru Impreza 1995 555 View_H.avif"
        ],
        "tahun": "1995 (Group A)",
        "specs": "Ej20 Boxer Turbo, 300 HP, AWD",
        "driver": "Colin McRae 🏴󠁧󠁢󠁳󠁣󠁴󠁿"
    },
    "Subaru WRX STi NR4": {
        "images": [
            "images/Subaru WRX STi NR4 View_A.avif", "images/Subaru WRX STi NR4 View_B.avif", "images/Subaru WRX STi NR4 View_C.avif",
            "images/Subaru WRX STi NR4 View_D.avif", "images/Subaru WRX STi NR4 View_E.avif", "images/Subaru WRX STi NR4 View_F.avif",
            "images/Subaru WRX STi NR4 View_G.avif", "images/Subaru WRX STi NR4 View_H.avif"
        ],
        "tahun": "2015 (Production Cup)",
        "specs": "2.0L Boxer Turbo, 280 HP, AWD",
        "driver": "Mark Higgins 🇬🇧"
    }
}

# --- ENDPOINT API (Pintu Masuk Client) ---
@app.get("/api/wrc_data")
def get_all_cars():
    # Server ngasih data ke siapa aja yang minta
    return gallery_data

# Kalau mau dijalankan langsung dari tombol play VS Code
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)