"""
[MODEL] db_models.py
Mengendalikan interaksi data dengan MySQL / TiDB Cloud untuk entiti:
- Foundation
- Lipstick
"""

import mysql.connector
from config import get_db_config

# Urutan kecerahan skintone (fair -> deep tan)
SKINTONE_ORDER = [
    "fair", "light medium", "medium",
    "light tan", "medium tan", "tan", "deep tan"
]


def get_connection():
    """Membuka sambungan ke pangkalan data."""
    return mysql.connector.connect(**get_db_config())


def check_connection():
    """Semak kesihatan sambungan DB + bilangan baris."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM foundation")
        n_f = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM lipstick")
        n_l = cur.fetchone()[0]
        cur.close()
        conn.close()
        return True, f"MySQL OK (foundation: {n_f} baris, lipstick: {n_l} baris)"
    except mysql.connector.Error as err:
        return False, f"MySQL GAGAL: {err} -> semak tetapan DB atau persekitaran"


def get_recommendations(undertone, skintone):
    """
    Mengambil cadangan warna foundation berdasarkan undertone dan skintone.
    Jika tiada padanan tepat, cari skintone paling hampir.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Padanan tepat
        cursor.execute(
            "SELECT shade, skintone FROM foundation "
            "WHERE undertone = %s AND skintone = %s LIMIT 1",
            (undertone, skintone)
        )
        exact = cursor.fetchone()

        if exact:
            cursor.close()
            conn.close()
            return [exact]

        # 2) Padanan terdekat jika tiada tepat
        cursor.execute(
            "SELECT shade, skintone FROM foundation WHERE undertone = %s",
            (undertone,)
        )
        candidates = cursor.fetchall()
        cursor.close()
        conn.close()

        if not candidates:
            return []

        def distance(row):
            try:
                return abs(
                    SKINTONE_ORDER.index(row["skintone"])
                    - SKINTONE_ORDER.index(skintone)
                )
            except ValueError:
                return 999

        best_match = min(candidates, key=distance)
        return [best_match]

    except mysql.connector.Error as err:
        print("[DB Error]:", err)
        return []


def get_lipstick_recommendations(undertone, skintone):
    """
    Mengambil cadangan warna lipstick berdasarkan undertone dan skintone.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Padanan tepat
        cursor.execute(
            "SELECT shade, skintone, undertone FROM lipstick "
            "WHERE undertone = %s AND skintone = %s LIMIT 1",
            (undertone, skintone)
        )
        exact = cursor.fetchone()

        if exact:
            cursor.close()
            conn.close()
            return [exact]

        # Padanan terdekat
        cursor.execute(
            "SELECT shade, skintone, undertone FROM lipstick WHERE undertone = %s",
            (undertone,)
        )
        candidates = cursor.fetchall()
        cursor.close()
        conn.close()

        if not candidates:
            return []

        def distance(row):
            try:
                return abs(
                    SKINTONE_ORDER.index(row["skintone"])
                    - SKINTONE_ORDER.index(skintone)
                )
            except ValueError:
                return 999

        best_match = min(candidates, key=distance)
        return [best_match]

    except mysql.connector.Error as err:
        print("[DB Error]:", err)
        return []
