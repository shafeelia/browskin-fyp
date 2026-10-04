import cv2
import joblib
import os
import pandas as pd

from undertone_utils import extract_features

# Load model
model = joblib.load("knn_model.pkl")
scaler = joblib.load("scaler.pkl")

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
        print("[FAIL] Cannot read:", filename)
        continue

    feat = extract_features(image)

    if feat is None:
        print("[FAIL] Tak jumpa muka/pipi yang sah:", filename)
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
    print("[SUCCESS] Prediction:", prediction)

print("\n===================================")
print("TEST COMPLETE")
print("===================================")
