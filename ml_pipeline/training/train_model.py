import os
import sys
import pandas as pd
import cv2

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.join(ML_DIR, "utils"))

try:
    from undertone_utils import extract_features
except ImportError:
    from utils.undertone_utils import extract_features

# Lokasi dataset
base_path = os.path.join(ML_DIR, "dataset")
if not os.path.exists(base_path):
    base_path = "dataset"

categories = ["cool", "neutral", "olive", "warm"]

results = []
skipped = []

for category in categories:

    folder = os.path.join(base_path, category)

    for filename in os.listdir(folder):

        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(folder, filename)

        image = cv2.imread(image_path)

        if image is None:
            skipped.append((filename, "gagal baca gambar"))
            continue

        feat = extract_features(image)

        if feat is None:
            skipped.append((filename, "tak jumpa muka/pipi yang sah"))
            continue

        results.append([
            filename,
            category,
            feat["R"],
            feat["G"],
            feat["B"],
            feat["H"],
            feat["S"],
            feat["V"],
            feat["rn"],
            feat["gn"],
            feat["bn"],
            feat["method"]
        ])


# Create DataFrame
columns = [
    "filename",
    "undertone",
    "R",
    "G",
    "B",
    "H",
    "S",
    "V",
    "rn",
    "gn",
    "bn",
    "method"
]

df = pd.DataFrame(results, columns=columns)

print("===================================")
print("DATASET PROCESSING COMPLETE")
print("===================================")

print("Total gambar berjaya diproses:", len(df))
print("\nImages by undertone:")
print(df["undertone"].value_counts())

print("\nMethod breakdown (face_detected = automatik jumpa muka, fallback = guna crop peratusan):")
print(df["method"].value_counts())

if skipped:
    print("\n⚠️  Gambar DILANGKAU (tak diproses) — semak gambar ni:")
    for fn, reason in skipped:
        print(f"   - {fn}: {reason}")

# Save extracted data (buang column 'method' sebelum save, sebab train_knn.py tak perlukan)
output_csv = os.path.join(ML_DIR, "data", "undertone_features.csv")
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df.drop(columns=["method"]).to_csv(output_csv, index=False)
df.drop(columns=["method"]).to_csv("undertone_features.csv", index=False)

print(f"\n✅ Features saved to: {output_csv}")
