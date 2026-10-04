"""
[MODEL] undertone_model.py
Mengendalikan pengecaman wajah (Haar Cascade), ekstraksi ciri warna kulit (RGB, HSV, Chromaticity),
dan ramalan undertone berasaskan model Machine Learning (KNN Classifier).
"""

import os
import cv2
import joblib
import numpy as np
import pandas as pd
from config import KNN_MODEL_PATH, SCALER_PATH


class UndertoneModel:
    """Model Machine Learning bagi pengecaman undertone & ciri kulit."""

    def __init__(self, model_path=KNN_MODEL_PATH, scaler_path=SCALER_PATH):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self._face_cascade = None
        try:
            if hasattr(cv2, "CascadeClassifier") and hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
                self._face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                )
        except Exception as e:
            print(f"[Warning] Tidak dapat memuatkan Haar Cascade: {e}")
        self.load_model()

    def load_model(self):
        """Memuat turun model KNN dan Scaler dari disk."""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
        else:
            print(f"⚠️ Fail model tidak dijumpai di {self.model_path} / {self.scaler_path}")

    @staticmethod
    def classify_skintone(R, G, B):
        """
        Klasifikasi skintone berdasarkan formula luminance:
        Luminance = 0.299*R + 0.587*G + 0.114*B
        """
        luminance = 0.299 * R + 0.587 * G + 0.114 * B
        if luminance >= 190:
            return "fair"
        elif luminance >= 170:
            return "light medium"
        elif luminance >= 150:
            return "medium"
        elif luminance >= 145:
            return "light tan"
        elif luminance >= 140:
            return "medium tan"
        elif luminance >= 136:
            return "tan"
        else:
            return "deep tan"

    def _get_cheek_crops_from_face_box(self, image, x, y, w, h):
        """Crop pipi kiri dan kanan dari kotak wajah yang dikesan."""
        left_cheek = image[
            y + int(h * 0.55): y + int(h * 0.75),
            x + int(w * 0.12): x + int(w * 0.32)
        ]
        right_cheek = image[
            y + int(h * 0.55): y + int(h * 0.75),
            x + int(w * 0.68): x + int(w * 0.88)
        ]
        return left_cheek, right_cheek

    def _get_cheek_crops_fallback(self, image):
        """Fallback crop sekiranya pengesan wajah tidak menemui muka."""
        h, w, _ = image.shape
        face_crop = image[
            int(h * 0.25):int(h * 0.80),
            int(w * 0.20):int(w * 0.80)
        ]
        fh, fw, _ = face_crop.shape
        left_cheek = face_crop[
            int(fh * 0.45):int(fh * 0.68),
            int(fw * 0.18):int(fw * 0.42)
        ]
        right_cheek = face_crop[
            int(fh * 0.45):int(fh * 0.68),
            int(fw * 0.62):int(fw * 0.86)
        ]
        return left_cheek, right_cheek

    def extract_features(self, image):
        """
        Menerima imej cv2 BGR, mengesan wajah & pipi,
        dan mengekstrak ciri warna (RGB, HSV, normalized chromaticity).
        """
        if image is None:
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = ()
        if self._face_cascade is not None and not self._face_cascade.empty():
            faces = self._face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
            )

        method = "fallback"
        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            left_cheek, right_cheek = self._get_cheek_crops_from_face_box(image, x, y, w, h)
            method = "face_detected"
        else:
            left_cheek, right_cheek = self._get_cheek_crops_fallback(image)

        if left_cheek.size == 0 or right_cheek.size == 0:
            return None

        left_rgb = cv2.cvtColor(left_cheek, cv2.COLOR_BGR2RGB).mean(axis=(0, 1))
        right_rgb = cv2.cvtColor(right_cheek, cv2.COLOR_BGR2RGB).mean(axis=(0, 1))
        average_rgb = (left_rgb + right_rgb) / 2

        rgb_pixel = np.uint8([[average_rgb]])
        hsv_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_RGB2HSV)
        H, S, V = hsv_pixel[0][0]

        R_val, G_val, B_val = float(average_rgb[0]), float(average_rgb[1]), float(average_rgb[2])
        total = R_val + G_val + B_val
        if total <= 0:
            return None

        rn = R_val / total
        gn = G_val / total
        bn = B_val / total

        return {
            "R": round(R_val, 2),
            "G": round(G_val, 2),
            "B": round(B_val, 2),
            "H": int(H),
            "S": int(S),
            "V": int(V),
            "rn": round(rn, 5),
            "gn": round(gn, 5),
            "bn": round(bn, 5),
            "skintone": self.classify_skintone(R_val, G_val, B_val),
            "method": method
        }

    def predict(self, feat):
        """
        Menjalankan ramalan undertone menggunakan KNN Classifier
        dan mengira peratusan keyakinan (confidence).
        """
        if self.model is None or self.scaler is None:
            raise RuntimeError("Model AI atau Scaler belum dimuat turun.")

        features_df = pd.DataFrame(
            [[feat["rn"], feat["gn"], feat["bn"]]],
            columns=["rn", "gn", "bn"]
        )

        features_scaled = self.scaler.transform(features_df)
        prediction = self.model.predict(features_scaled)[0]

        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = round(float(max(probabilities)) * 100, 1)

        return str(prediction), confidence
