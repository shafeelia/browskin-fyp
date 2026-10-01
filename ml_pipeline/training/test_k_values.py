"""
Cuba beberapa nilai k (n_neighbors) untuk cari yang paling sesuai
dengan dataset korang sekarang. Run ni lepas train_model.py
(perlukan undertone_features.csv terkini).
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

import os

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "undertone_features.csv")
if not os.path.exists(CSV_PATH):
    CSV_PATH = "undertone_features.csv"

df = pd.read_csv(CSV_PATH)
X = df[["R", "G", "B", "H", "S", "V"]]
y = df["undertone"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("===================================")
print("TEST PELBAGAI NILAI K")
print("===================================")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

best_k = None
best_score = 0

for k in [3, 5, 7, 9, 11, 13, 15]:
    model = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(model, X_scaled, y, cv=cv)
    avg = scores.mean()
    print(f"k={k}: accuracy purata = {round(avg*100, 2)}%")
    if avg > best_score:
        best_score = avg
        best_k = k

print()
print(f"✅ Nilai k PALING BAIK: {best_k} (accuracy: {round(best_score*100,2)}%)")
print(f"   -> Tukar 'n_neighbors=3' dalam train_knn.py kepada 'n_neighbors={best_k}'")