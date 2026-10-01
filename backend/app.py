"""
Aplikasi Utama BrownSkin (MVC Architecture Entry Point).
Menguruskan laluan web (routes), inisialisasi Flask, dan memuatkan model AI.
"""

import os
import joblib
from flask import Flask, send_file, send_from_directory, request
from flask_cors import CORS

from config import WEBSITE_DIR, KNN_MODEL_PATH, SCALER_PATH
from models.db_models import check_connection
from controllers.predict_controller import handle_predict_request

app = Flask(__name__)
CORS(app)

# ========================================================
# [M - MODEL] Muat model Machine Learning & Scaler
# ========================================================
model = joblib.load(KNN_MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# ========================================================
# [V - VIEW] Laluan Paparan Antara Muka Pengguna (Frontend)
# ========================================================
@app.route("/")
def home():
    """Menyajikan halaman utama BrownSkin."""
    return send_from_directory(WEBSITE_DIR, "home.html")


@app.route("/test-upload")
def test_upload_page():
    """Halaman ujian ringkas untuk semakan diagnosis API."""
    test_page = os.path.join(WEBSITE_DIR, "test_upload.html")
    if os.path.exists(test_page):
        return send_file(test_page)
    return send_file(os.path.join(os.path.dirname(__file__), "index.html"))


@app.route("/<path:filename>")
def website_files(filename):
    """Menyajikan aset statik (CSS, JS, Imej) dari folder website dengan sokongan sub-folder automatik."""
    # 1. Semak laluan tepat dalam website/
    direct_path = os.path.join(WEBSITE_DIR, filename)
    if os.path.exists(direct_path) and os.path.isfile(direct_path):
        return send_from_directory(WEBSITE_DIR, filename)

    # 2. Semak dalam sub-folder tersusun (fallback automatik)
    subfolders = [
        "images",
        "images/banners",
        "images/products",
        "images/shades",
        "css",
        "js",
        "pages"
    ]
    for sub in subfolders:
        candidate = os.path.join(WEBSITE_DIR, sub, filename)
        if os.path.exists(candidate) and os.path.isfile(candidate):
            return send_from_directory(os.path.join(WEBSITE_DIR, sub), filename)

    return send_from_directory(WEBSITE_DIR, filename)


# ========================================================
# [C - CONTROLLER] Laluan API Pengesanan & Cadangan
# ========================================================
@app.route("/predict", methods=["POST"])
def predict():
    """Mengendalikan permintaan pengesanan muka melalui Predict Controller."""
    return handle_predict_request(request, model, scaler)


def _print_lan_url():
    """Membantu memaparkan alamat IP tempatan untuk ujian WiFi/telefon."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "127.0.0.1"

    port = int(os.environ.get("PORT", 5000))
    print("\n===================================")
    print("✨ BrownSkin MVC Server Berjalan ✨")
    print("===================================")
    print(f"  Laptop (Tempatan) : http://127.0.0.1:{port}")
    print(f"  Telefon (WiFi)    : http://{ip}:{port}")
    print("  Status Pangkalan Data:", check_connection()[1])
    print("===================================\n")


if __name__ == "__main__":
    _print_lan_url()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)