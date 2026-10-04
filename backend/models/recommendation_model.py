"""
[MODEL] recommendation_model.py
Mengendalikan operasi data MySQL untuk cadangan Foundation & Lipstick.
"""

import mysql.connector
from config import DB_CONFIG, SKINTONE_ORDER


class RecommendationModel:
    """Model data bagi cadangan produk mengikut undertone & skintone."""

    @staticmethod
    def check_connection():
        """Semak status sambungan MySQL. Mengembalikan (status: bool, mesej: str)."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM foundation")
            n_f = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM lipstick")
            n_l = cur.fetchone()[0]
            cur.close()
            conn.close()
            return True, f"MySQL OK (foundation: {n_f} baris, lipstick: {n_l} baris)"
        except Exception as err:
            return False, f"MySQL tidak aktif: {err} -> Sila buka XAMPP & jalankan MySQL."

    @staticmethod
    def get_foundation_recommendation(undertone, skintone):
        """
        Dapatkan cadangan foundation untuk padanan undertone & skintone.
        Menggunakan padanan tepat, atau skintone paling hampir sebagai fallback.
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # 1) Cuba padanan tepat
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

            # 2) Fallback: Cari skintone terdekat dalam undertone sama
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

        except Exception as err:
            print("[MySQL Error] Foundation query failed:", str(err))
            return []

    @staticmethod
    def get_lipstick_recommendation(undertone, skintone):
        """
        Dapatkan cadangan lipstick untuk padanan undertone & skintone.
        Menggunakan padanan tepat, atau skintone paling hampir sebagai fallback.
        """
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # 1) Padanan tepat
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

            # 2) Fallback: Cari pilihan undertone sama
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

        except Exception as err:
            print("[MySQL Error] Lipstick query failed:", str(err))
            return []
