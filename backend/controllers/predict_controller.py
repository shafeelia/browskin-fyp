"""
[CONTROLLER] predict_controller.py
Mengendalikan kitaran hidup permintaan pengesanan undertone:
1. Membaca fail imej daripada HTTP request.
2. Mengekstrak ciri warna kulit (Haar Cascade & color conversion).
3. Mengaplikasikan penskalaan (StandardScaler) & ramalan k-NN.
4. Mendapatkan cadangan produk foundation & lipstick daripada Database Model.
5. Memulangkan respons JSON berstruktur kepada Frontend (View).
"""

import cv2
import numpy as np
import pandas as pd
from flask import jsonify

try:
    from utils.undertone_utils import extract_features
except ImportError:
    from undertone_utils import extract_features

from models.db_models import get_recommendations, get_lipstick_recommendations


def handle_predict_request(request, model, scaler):
    """
    Memproses endpoint /predict.
    Mengembalikan (json_response, status_code).
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "Cannot read image"}), 400

    feat = extract_features(image)
    if feat is None:
        return jsonify({
            "error": "Tak dapat kesan muka/pipi dengan jelas. Sila muat naik gambar muka yang menghadap kamera dengan pencahayaan cukup terang."
        }), 422

    # Penskalaan ciri (rn, gn, bn)
    features_df = pd.DataFrame(
        [[feat["rn"], feat["gn"], feat["bn"]]],
        columns=["rn", "gn", "bn"]
    )
    features_scaled = scaler.transform(features_df)

    # Ramalan k-NN
    prediction = model.predict(features_scaled)[0]

    # Keyakinan ramalan (k-nearest neighbors agreement)
    probabilities = model.predict_proba(features_scaled)[0]
    confidence = round(float(max(probabilities)) * 100, 1)

    # Cadangan produk daripada Model
    undertone_str = str(prediction)
    skintone_str = feat["skintone"]
    foundation_recs = get_recommendations(undertone_str, skintone_str)
    lipstick_recs = get_lipstick_recommendations(undertone_str, skintone_str)

    return jsonify({
        "R": feat["R"],
        "G": feat["G"],
        "B": feat["B"],
        "H": feat["H"],
        "S": feat["S"],
        "V": feat["V"],
        "undertone": undertone_str,
        "skintone": skintone_str,
        "confidence": confidence,
        "detection_method": feat["method"],
        "recommendations": foundation_recs,
        "lipstick_recommendations": lipstick_recs
    }), 200
