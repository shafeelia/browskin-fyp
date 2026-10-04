"""
Aplikasi Utama BrownSkin (Seni Bina MVC)
Entry Point pelayan Flask.
"""

import socket
from flask import Flask
from flask_cors import CORS

from config import WEBSITE_DIR
from controllers.page_controller import page_bp
from controllers.prediction_controller import prediction_bp
from models.recommendation_model import RecommendationModel


def create_app():
    """Fungsi factory untuk mencipta dan mengkonfigurasi aplikasi Flask."""
    app = Flask(__name__, static_folder=WEBSITE_DIR)
    CORS(app)

    # Daftar Controllers (Blueprints)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(page_bp)

    return app


app = create_app()


def print_lan_url():
    """Papar maklumat akses IP tempatan dan WiFi."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "127.0.0.1"

    _, db_status = RecommendationModel.check_connection()

    print("\n===================================")
    print("BrownSkin Server Sedang Berjalan (MVC)")
    print("===================================")
    print(f"  Di komputer ini      : http://127.0.0.1:5000")
    print(f"  Dari telefon (WiFi)  : http://{ip}:5000")
    print("  Pastikan telefon & laptop bersambung ke WiFi yang SAMA.")
    print(f"  Database             : {db_status}")
    print("===================================\n")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print_lan_url()
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)