import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load extracted features
df = pd.read_csv("undertone_features.csv")

# Features: guna normalized chromaticity (rn, gn, bn) sahaja.
#
# Diuji secara empirik (lihat backend/test_k_values.py, 5-fold
# cross-validation diulang dengan 10 random_state berbeza) -- rn/gn/bn
# secara konsisten bagi accuracy purata ~66% berbanding ~52% kalau guna
# R, G, B, H, S, V mentah.
#
# Sebabnya: rn = R/(R+G+B), begitu juga gn & bn. Formula ni
# "menyingkirkan" kesan kecerahan keseluruhan (brightness/lighting) --
# jadi ciri ni fokus kepada NISBAH warna (lebih berkait dgn undertone)
# berbanding kecerahan mentah (lebih berkait dgn skintone, bukan
# undertone). Ini sebab kenapa gambar diambil dalam lighting berbeza
# tapi undertone sama, boleh jadi lebih konsisten diklasifikasi.
X = df[["rn", "gn", "bn"]]

# Target
y = df["undertone"]


# =========================
# Cari k (n_neighbors) paling sesuai dulu guna cross-validation,
# supaya nombor k bukan dipilih secara rawak/agak-agak.
# =========================
scaler_cv = StandardScaler()
X_scaled_cv = scaler_cv.fit_transform(X)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

best_k = 3
best_score = 0

print("===================================")
print("CARI K PALING SESUAI (cross-validation)")
print("===================================")

for k in [3, 5, 7, 9, 11, 13, 15]:
    model_cv = KNeighborsClassifier(n_neighbors=k, weights="uniform")
    scores = cross_val_score(model_cv, X_scaled_cv, y, cv=cv)
    avg = scores.mean()
    print(f"k={k}: accuracy purata = {round(avg * 100, 2)}%")
    if avg > best_score:
        best_score = avg
        best_k = k

print(f"\n[OK] k dipilih secara automatik: {best_k} (accuracy CV: {round(best_score * 100, 2)}%)")


# Split dataset (untuk laporan akhir sahaja - model sebenar yang
# disimpan nanti di-fit semula guna SEMUA data supaya tak bazir data
# latihan yang terhad, ~151 gambar sahaja)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Standardization
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# KNN model (k dipilih automatik di atas)
model = KNeighborsClassifier(n_neighbors=best_k, weights="uniform")

model.fit(X_train_scaled, y_train)


# Prediction
y_pred = model.predict(X_test_scaled)


# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n===================================")
print("KNN MODEL RESULTS (test split 80/20)")
print("===================================")

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))


# =========================
# Model FINAL yang disimpan: di-fit semula guna SEMUA data (bukan
# hanya 80%), supaya model produksi guna maklumat maksimum yang ada.
# Ini normal/standard practice: split di atas untuk ANGGARAN accuracy
# sahaja, model sebenar guna semua data yang ada.
# =========================
final_scaler = StandardScaler()
X_all_scaled = final_scaler.fit_transform(X)

final_model = KNeighborsClassifier(n_neighbors=best_k, weights="uniform")
final_model.fit(X_all_scaled, y)

# Save model
joblib.dump(final_model, "knn_model.pkl")
joblib.dump(final_scaler, "scaler.pkl")

print("\n[OK] KNN model saved as knn_model.pkl (k =", best_k, ", features = rn/gn/bn)")
print("[OK] Scaler saved as scaler.pkl")
