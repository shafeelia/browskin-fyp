"""
[CONTROLLER] page_controller.py
Mengendalikan permintaan paparan (Views) dan fail statik laman web.
"""

import os
from flask import Blueprint, send_from_directory, send_file
from config import WEBSITE_DIR, BACKEND_DIR

page_bp = Blueprint("page", __name__)


@page_bp.route("/")
def home():
    """Menyajikan halaman utama View (home.html)."""
    return send_from_directory(WEBSITE_DIR, "home.html")


@page_bp.route("/test-upload")
def test_upload():
    """Menyajikan halaman ujian diagnostik backend."""
    return send_file(os.path.join(BACKEND_DIR, "index.html"))


@page_bp.route("/<path:filename>")
def serve_website_assets(filename):
    """Menyajikan aset visual (CSS, JS, Imej) dari folder View (website)."""
    return send_from_directory(WEBSITE_DIR, filename)
