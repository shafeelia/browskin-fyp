"""
Shared logic untuk extract ciri warna kulit (RGB + HSV) dari gambar muka.
Digunakan oleh train_model.py, predict.py, dan app.py supaya semua
konsisten guna kaedah crop yang SAMA.
"""

import cv2
import numpy as np

# Load face detector sekali sahaja (reuse untuk setiap panggilan)
_face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def _get_cheek_crops_from_face_box(image, x, y, w, h):
    """Cara BARU: crop pipi berdasarkan kotak muka yang dikesan (x,y,w,h)."""
    left_cheek = image[
        y + int(h * 0.55): y + int(h * 0.75),
        x + int(w * 0.12): x + int(w * 0.32)
    ]
    right_cheek = image[
        y + int(h * 0.55): y + int(h * 0.75),
        x + int(w * 0.68): x + int(w * 0.88)
    ]
    return left_cheek, right_cheek


def _get_cheek_crops_fallback(image):
    """Cara LAMA: crop ikut peratusan saiz gambar keseluruhan.
    Dipakai HANYA bila muka tak dapat dikesan (contoh: gambar terlalu zoom)."""
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


def classify_skintone(R, G, B):
    """
    Kelaskan skintone berdasarkan LUMINANCE (kecerahan sebenar,
    formula piawai: 0.299R + 0.587G + 0.114B), bukan V (HSV Value).

    Sebab: V = max(R,G,B) bias tinggi untuk warna kulit yang
    "reddish"/warm walaupun kulit tu sebenarnya gelap. Luminance
    lebih tepat mencerminkan kecerahan macam mata manusia nampak.

    Nota PENTING: kategori ni heuristik ringkas (rule-based), BUKAN
    hasil training/machine learning -- dataset ni tiada label
    skintone sebenar (cuma label undertone). Accuracy terhad,
    terutama bila lighting gambar tak konsisten (gambar studio
    terang vs selfie biasa boleh bagi brightness berbeza utk skin
    tone yang sama org). Ini limitation yang elok didokumenkan
    dalam laporan (rujuk Weir et al. 2024 pasal cabaran skin tone
    assessment).
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


def extract_features(image):
    """
    Terima gambar (BGR, dari cv2.imread / cv2.imdecode).
    Return dict: {R, G, B, H, S, V, method} atau None kalau gambar tak sah.
    'method' = 'face_detected' atau 'fallback' (berguna untuk debug/logging).
    """
    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = _face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
    )

    method = "fallback"

    if len(faces) > 0:
        # Pilih muka paling besar (paling hampir/jelas)
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        left_cheek, right_cheek = _get_cheek_crops_from_face_box(image, x, y, w, h)
        method = "face_detected"
    else:
        left_cheek, right_cheek = _get_cheek_crops_fallback(image)

    if left_cheek.size == 0 or right_cheek.size == 0:
        return None

    left_rgb = cv2.cvtColor(left_cheek, cv2.COLOR_BGR2RGB).mean(axis=(0, 1))
    right_rgb = cv2.cvtColor(right_cheek, cv2.COLOR_BGR2RGB).mean(axis=(0, 1))
    average_rgb = (left_rgb + right_rgb) / 2

    rgb_pixel = np.uint8([[average_rgb]])
    hsv_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_RGB2HSV)
    H, S, V = hsv_pixel[0][0]

    # =========================
    # Normalized chromaticity (rn, gn, bn)
    # =========================
    # rn = R / (R+G+B), sama untuk gn dan bn.
    # Ni "menyingkirkan" kesan kecerahan/lighting keseluruhan (brightness)
    # daripada nisbah warna, jadi ciri ni lebih stabil merentas gambar
    # yang diambil dalam pencahayaan berbeza -- diuji secara empirik
    # (5-fold cross-validation berulang, backend/test_k_values.py) memberi
    # accuracy KNN jauh lebih tinggi (~66%) berbanding guna R,G,B,H,S,V
    # mentah sahaja (~52%). Ini sebab utama undertone_features.csv dan
    # train_knn.py kini guna rn/gn/bn sebagai ciri utama.
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
        "skintone": classify_skintone(R_val, G_val, B_val),
        "method": method
    }