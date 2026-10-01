import os

from flask import Flask, request, jsonify, send_file, send_from_directory
import joblib
import cv2
import numpy as np
import pandas as pd
from flask_cors import CORS

from undertone_utils import extract_features
from db_utils import get_recommendations, get_lipstick_recommendations, check_connection

# Folder "website" (HTML/CSS/JS/gambar) ada SEBELAH folder "backend".
# Flask serve terus dari sini supaya HANYA SATU server (satu URL/IP)
# perlu dibuka -- ini penting utk boleh buka dari fon: fon dan laptop
# kena guna URL/origin yang SAMA supaya fetch("/predict") dari
# script.js automatik sampai ke server yang betul (rujuk SERVER_URL
# dalam website/script.js).
WEBSITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "website")

app = Flask(__name__)
CORS(app)  # benarkan website BrownSkin panggil /predict walaupun origin lain
 
# Load model
model = joblib.load("knn_model.pkl")
scaler = joblib.load("scaler.pkl")


@app.route("/")
def home():
    # Buka terus halaman utama website sebenar (home.html), bukan
    # index.html (tu hanya alat ujian ringkas backend).
    return send_from_directory(WEBSITE_DIR, "home.html")


@app.route("/test-upload")
def test_upload_page():
    # Halaman ujian ringkas (upload terus, tanpa styling) -- berguna
    # untuk debug backend secara berasingan drpd website sebenar.
    return send_file("index.html")


@app.route("/<path:filename>")
def website_files(filename):
    # Serve semua fail lain dalam folder website (html/css/js/png...)
    # supaya link macam "about.html", "style.css", "logo.png" berfungsi.
    return send_from_directory(WEBSITE_DIR, filename)
 
 
@app.route("/predict", methods=["POST"])
def predict():
 
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})
 
    file = request.files["image"]
 
    # Read uploaded image
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
 
    if image is None:
        return jsonify({"error": "Cannot read image"})
 
    feat = extract_features(image)
 
    if feat is None:
        return jsonify({
            "error": "Tak dapat kesan muka/pipi dengan jelas. Sila muat naik gambar muka yang menghadap kamera, pencahayaan cukup terang."
        })
 
    # =========================
    # Scale (guna DataFrame supaya column names sepadan dgn masa training,
    # buang warning "X does not have valid feature names")
    # =========================
 
    features_df = pd.DataFrame(
        [[feat["rn"], feat["gn"], feat["bn"]]],
        columns=["rn", "gn", "bn"]
    )
 
    features_scaled = scaler.transform(features_df)
 
    # =========================
    # Prediction
    # =========================
 
    prediction = model.predict(features_scaled)[0]

    # Confidence: peratus jiran (k-nearest neighbours) yang bersetuju
    # dengan prediction ni. Bukan "accuracy" model, tapi keyakinan
    # untuk gambar SPESIFIK ni sahaja.
    probabilities = model.predict_proba(features_scaled)[0]
    confidence = round(float(max(probabilities)) * 100, 1)

    # =========================
    # Foundation Recommendation
    # =========================
 
    recommendations = get_recommendations(str(prediction), feat["skintone"])
    lipstick_recommendations = get_lipstick_recommendations(str(prediction), feat["skintone"])
 
    return jsonify({
        "R": feat["R"],
        "G": feat["G"],
        "B": feat["B"],
        "H": feat["H"],
        "S": feat["S"],
        "V": feat["V"],
        "undertone": str(prediction),
        "skintone": feat["skintone"],
        "confidence": confidence,
        "detection_method": feat["method"],
        "recommendations": recommendations,
        "lipstick_recommendations": lipstick_recommendations
    })
 
 
def _print_lan_url():
    """Bantu dapatkan IP laptop dalam WiFi/LAN yang sama, supaya senang
    tahu alamat mana nak taip dalam browser fon."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "127.0.0.1"
    print("\n===================================")
    print("BrownSkin server sedang berjalan")
    print("===================================")
    print(f"  Di laptop ni      : http://127.0.0.1:5000")
    print(f"  Dari fon (WiFi sama): http://{ip}:5000")
    print("Pastikan fon dan laptop sambung WiFi yang SAMA.")
    print("  Database          :", check_connection()[1])
    print("===================================\n")


if __name__ == "__main__":
    _print_lan_url()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)