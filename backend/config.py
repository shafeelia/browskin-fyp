"""
Tetapan Konfigurasi Projek BrownSkin (MVC Architecture)
"""

import os

# Direktori Utama
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
WEBSITE_DIR = os.path.join(PROJECT_ROOT, "website")  # Folder View untuk frontend
DATASET_DIR = os.path.join(BACKEND_DIR, "dataset")

# Fail Model AI
KNN_MODEL_PATH = os.path.join(BACKEND_DIR, "knn_model.pkl")
SCALER_PATH = os.path.join(BACKEND_DIR, "scaler.pkl")

# Pangkalan Data TiDB Cloud
DB_CONFIG = {
    "host": os.environ.get("BROWNSKIN_DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"),
    "port": int(os.environ.get("BROWNSKIN_DB_PORT", 4000)),
    "user": os.environ.get("BROWNSKIN_DB_USER", "2cPx11MtXzY5S1d.root"),
    "password": os.environ.get("BROWNSKIN_DB_PASSWORD", "ZisDDkQiIaus8Wzy"),
    "database": os.environ.get("BROWNSKIN_DB_NAME", "brownskin"),
    "ssl_verify_cert": True,
    "ssl_verify_identity": True,
}

# Urutan skintone dari cerah -> gelap (untuk proximity matching)
SKINTONE_ORDER = [
    "fair", "light medium", "medium",
    "light tan", "medium tan", "tan", "deep tan"
]
