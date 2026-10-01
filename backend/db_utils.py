"""
Modul untuk sambung ke MySQL (XAMPP) dan ambil cadangan foundation
berdasarkan undertone + skintone yang dikesan.
"""

import os

import mysql.connector

def get_db_config():
    cfg = {
        "host": os.environ.get("BROWNSKIN_DB_HOST", "localhost"),
        "port": int(os.environ.get("BROWNSKIN_DB_PORT", 3307)),
        "user": os.environ.get("BROWNSKIN_DB_USER", "root"),
        "password": os.environ.get("BROWNSKIN_DB_PASSWORD", ""),
        "database": os.environ.get("BROWNSKIN_DB_NAME", "brownskin"),
    }
    # Jika bersambung ke TiDB Cloud atau mana-mana cloud database
    if "tidbcloud.com" in cfg["host"] or os.environ.get("BROWNSKIN_DB_SSL", "").lower() in ("true", "1"):
        cfg["ssl_disabled"] = False
    return cfg


def get_connection():
    return mysql.connector.connect(**get_db_config())


def check_connection():
    """Semak sambungan DB + bilangan baris. Return (ok: bool, mesej: str).
    Dipanggil bila server start supaya masalah DB nampak awal."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM foundation")
        n_f = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM lipstick")
        n_l = cur.fetchone()[0]
        cur.close()
        conn.close()
        return True, f"MySQL OK  (foundation: {n_f} baris, lipstick: {n_l} baris)"
    except mysql.connector.Error as err:
        return False, f"MySQL GAGAL: {err}  -> semak tetapan DB atau jalankan setup"


# Urutan skintone dari paling cerah -> paling gelap.
# Digunakan untuk cari skintone PALING HAMPIR kalau tiada match tepat
# dalam database untuk kombinasi undertone+skintone tertentu.
SKINTONE_ORDER = [
    "fair", "light medium", "medium",
    "light tan", "medium tan", "tan", "deep tan"
]


def get_recommendations(undertone, skintone):
    """
    Terima undertone (contoh: 'warm') dan skintone (contoh: 'medium').
    Return SATU cadangan sahaja: [{"shade": "...", "skintone": "..."}]
    Kalau tiada match tepat, cari skintone yang PALING HAMPIR dalam
    undertone yang sama. Return [] kalau langsung tiada data untuk
    undertone tu, atau connection gagal.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Cuba match tepat: undertone + skintone
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

        # 2) Tiada match tepat -> ambil semua produk untuk undertone ni,
        #    pilih skintone yang paling hampir ikut SKINTONE_ORDER
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
                return 999  # skintone tak dikenali, letak paling jauh

        best_match = min(candidates, key=distance)
        return [best_match]

    except mysql.connector.Error as err:
        print("❌ MySQL Error:", err)
        return []


def get_lipstick_recommendations(undertone, skintone):
    """
    Sama logik macam get_recommendations(), tapi query table 'lipstick'.
    Return SATU cadangan sahaja: [{"shade": "...", "skintone": "...", "undertone": "..."}]
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Cari match tepat
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

        # Kalau tiada match tepat, cari lipstick dengan undertone sama
        cursor.execute(
            "SELECT shade, skintone, undertone FROM lipstick "
            "WHERE undertone = %s",
            (undertone,)
        )

        candidates = cursor.fetchall()

        cursor.close()
        conn.close()

        if not candidates:
            return []

        # Cari skintone paling hampir
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
        print("❌ MySQL Error:", err)
        return []