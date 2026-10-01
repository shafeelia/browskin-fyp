"""
Konfigurasi Pusat Aplikasi BrownSkin (Backend).
Menguruskan laluan direktori (paths) dan tetapan sambungan pangkalan data (MySQL / TiDB).
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
WEBSITE_DIR = os.path.join(PROJECT_ROOT, "website")
MODELS_DIR = os.path.join(BASE_DIR, "models", "saved_models")

# Fail model yang telah dilatih
KNN_MODEL_PATH = os.path.join(MODELS_DIR, "knn_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")

# Fallback ke folder backend jika tiada dalam models/saved_models
if not os.path.exists(KNN_MODEL_PATH):
    KNN_MODEL_PATH = os.path.join(BASE_DIR, "knn_model.pkl")
if not os.path.exists(SCALER_PATH):
    SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")


def get_db_config():
    """Mengembalikan konfigurasi sambungan pangkalan data."""
    host = os.environ.get("BROWNSKIN_DB_HOST", "localhost")
    default_db = "brownskin" if "tidbcloud.com" in host else "undertone detection"
    cfg = {
        "host": host,
        "port": int(os.environ.get("BROWNSKIN_DB_PORT", 3307)),
        "user": os.environ.get("BROWNSKIN_DB_USER", "root"),
        "password": os.environ.get("BROWNSKIN_DB_PASSWORD", ""),
        "database": os.environ.get("BROWNSKIN_DB_NAME", default_db),
    }
    # Sambungan SSL automatik untuk TiDB Cloud
    if "tidbcloud.com" in cfg["host"] or os.environ.get("BROWNSKIN_DB_SSL", "").lower() in ("true", "1"):
        cfg["ssl_disabled"] = False
    return cfg
