import cv2
import joblib
import os
import pandas as pd

import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.join(ML_DIR, "utils"))

try:
    from undertone_utils import extract_features
except ImportError:
    from utils.undertone_utils import extract_features

# Load model
model_path = os.path.join(ML_DIR, "..", "backend", "models", "saved_models", "knn_model.pkl")
scaler_path = os.path.join(ML_DIR, "..", "backend", "models", "saved_models", "scaler.pkl")
if not os.path.exists(model_path):
    model_path = "knn_model.pkl"
    scaler_path = "scaler.pkl"

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

test_folder = os.path.join(ML_DIR, "test_images")
if not os.path.exists(test_folder):
    test_folder = "test_images"

print("===================================")
print("TESTING MULTIPLE IMAGES")
print("===================================")

for filename in os.listdir(test_folder):

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(test_folder, filename)

    image = cv2.imread(image_path)

    if image is None:
        print("❌ Cannot read:", filename)
        continue

    feat = extract_features(image)

    if feat is None:
        print("❌ Tak jumpa muka/pipi yang sah:", filename)
        continue

    features_df = pd.DataFrame(
        [[feat["rn"], feat["gn"], feat["bn"]]],
        columns=["rn", "gn", "bn"]
    )

    features_scaled = scaler.transform(features_df)

    prediction = model.predict(features_scaled)[0]

    print("\nImage:", filename)
    print("RGB:", feat["R"], feat["G"], feat["B"])
    print("HSV:", feat["H"], feat["S"], feat["V"])
    print("Method:", feat["method"])
    print("[OK] Prediction:", prediction)

print("\n===================================")
print("TEST COMPLETE")
print("===================================")
