"""
[CONTROLLER] prediction_controller.py
Mengendalikan endpoint API /predict bagi pemprosesan imej, analisis AI,
dan pengeluaran cadangan foundation & lipstick.
"""

import cv2
import numpy as np
from flask import Blueprint, request, jsonify
from models.undertone_model import UndertoneModel
from models.recommendation_model import RecommendationModel

prediction_bp = Blueprint("prediction", __name__)

# Inisialisasi Model AI (Singleton dalam controller)
undertone_model = UndertoneModel()


@prediction_bp.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint pemprosesan pengesanan kulit:
    1. Pengesahan input fail imej
    2. Model AI ekstraksi ciri & pengelasan skintone
    3. Model AI ramalan undertone & confidence
    4. Model Rekomendasi carian produk foundation & lipstick
    5. Menghantar respon JSON lengkap kepada View
    """
    if "image" not in request.files:
        return jsonify({"error": "Tiada gambar dimuat naik"}), 400

    file = request.files["image"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "Gagal membaca format gambar"}), 400

    # 1. Model: Ekstrak ciri warna kulit
    feat = undertone_model.extract_features(image)
    if feat is None:
        return jsonify({
            "error": "Tak dapat kesan muka/pipi dengan jelas. Sila muat naik gambar muka yang menghadap kamera dengan pencahayaan terang."
        }), 422

    # 2. Model: Ramalan undertone & confidence
    try:
        prediction, confidence = undertone_model.predict(feat)
    except Exception as e:
        return jsonify({"error": f"Ralat semasa inferens model: {str(e)}"}), 500

    # 3. Model: Dapatkan cadangan produk dari database
    recommendations = RecommendationModel.get_foundation_recommendation(prediction, feat["skintone"])
    lipstick_recommendations = RecommendationModel.get_lipstick_recommendation(prediction, feat["skintone"])

    # 4. Respon JSON kembali kepada View
    return jsonify({
        "R": feat["R"],
        "G": feat["G"],
        "B": feat["B"],
        "H": feat["H"],
        "S": feat["S"],
        "V": feat["V"],
        "undertone": prediction,
        "skintone": feat["skintone"],
        "confidence": confidence,
        "detection_method": feat["method"],
        "recommendations": recommendations,
        "lipstick_recommendations": lipstick_recommendations
    })
