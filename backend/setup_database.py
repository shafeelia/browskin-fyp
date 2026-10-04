"""
Cipta database dan import ../database/undertone_detection.sql
(table foundation + lipstick). Jalankan untuk memuat naik atau mengemaskini data:

    cd backend
    python setup_database.py

Menyokong kedua-dua MySQL tempatan (XAMPP) dan TiDB Cloud mengikut config.py.
"""
import os
import re
import sys

import mysql.connector

from config import DB_CONFIG

SQL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "database", "undertone_detection.sql")


def load_statements(path):
    text = open(path, encoding="utf-8").read()
    # Buang conditional comment phpMyAdmin
    text = re.sub(r"/\*!.*?\*/;?", "", text, flags=re.S)
    
    # Jadikan `id` AUTO_INCREMENT PRIMARY KEY terus dalam CREATE TABLE (keperluan wajib TiDB Cloud)
    text = re.sub(r"`id`\s+int\(\d+\)\s+NOT\s+NULL", "`id` int(100) NOT NULL AUTO_INCREMENT PRIMARY KEY", text, flags=re.IGNORECASE)

    lines = [l for l in text.splitlines() if not l.lstrip().startswith("--")]
    stmts = [s.strip() for s in "\n".join(lines).split(";") if s.strip()]

    clean_stmts = []
    for s in stmts:
        u = s.upper()
        if u in ("START TRANSACTION", "COMMIT") or u.startswith(("SET SQL_MODE", "SET TIME_ZONE")):
            continue
        # Abaikan arahan ALTER TABLE ADD/MODIFY AUTO_INCREMENT phpMyAdmin sebab sudah dimasukkan secara inline
        if "ADD PRIMARY KEY" in u or ("AUTO_INCREMENT" in u and u.startswith("ALTER TABLE")):
            continue
        clean_stmts.append(s)

    return clean_stmts


def main():
    db = DB_CONFIG["database"]
    connect_args = {k: v for k, v in DB_CONFIG.items() if k != "database"}

    try:
        conn = mysql.connector.connect(**connect_args)
    except mysql.connector.Error as err:
        sys.exit(f"Tak dapat sambung ke pangkalan data: {err}\n"
                 "Semak tetapan dalam config.py.")

    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    cur.execute(f"USE `{db}`")
    cur.execute("DROP TABLE IF EXISTS `foundation`")
    cur.execute("DROP TABLE IF EXISTS `lipstick`")

    n = 0
    for stmt in load_statements(SQL_FILE):
        cur.execute(stmt)
        n += 1
    conn.commit()

    for t in ("foundation", "lipstick"):
        cur.execute(f"SELECT COUNT(*) FROM `{t}`")
        print(f"  {t}: {cur.fetchone()[0]} baris")
    print(f"Siap -- pangkalan data '{db}' sedia ({n} statement dijalankan).")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
