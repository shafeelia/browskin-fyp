"""
Cipta database `undertone detection` dan import ../database/undertone_detection.sql
(table foundation + lipstick). Jalankan SEKALI sebelum start server:

    cd backend
    python setup_database.py

Pastikan MySQL di XAMPP dah Start. Tetapan sambungan ikut db_utils.py.
Selamat dijalankan berulang kali (table lama akan di-reset ikut fail .sql).
"""
import os
import re
import sys

DB_CONFIG = {
    "host": os.environ.get("BROWNSKIN_DB_HOST", "localhost"),
    "port": int(os.environ.get("BROWNSKIN_DB_PORT", 3307)),
    "user": os.environ.get("BROWNSKIN_DB_USER", "root"),
    "password": os.environ.get("BROWNSKIN_DB_PASSWORD", ""),
    "database": os.environ.get("BROWNSKIN_DB_NAME", "brownskin"),
}

SQL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "undertone_detection.sql")


def load_statements(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"/\*!.*?\*/;?", "", text, flags=re.S)          # buang conditional comment phpMyAdmin
    lines = [l for l in text.splitlines() if not l.lstrip().startswith("--")]
    return [s.strip() for s in "\n".join(lines).split(";") if s.strip()]


def main():
    db = DB_CONFIG["database"]
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG.get("port", 3307),
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
    except mysql.connector.Error as err:
        sys.exit(f"Tak dapat sambung ke MySQL: {err}\n"
                 "Semak XAMPP dah Start dan user/password dalam db_utils.py.")

    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    cur.execute(f"USE `{db}`")
    cur.execute("DROP TABLE IF EXISTS `foundation`")
    cur.execute("DROP TABLE IF EXISTS `lipstick`")

    n = 0
    for stmt in load_statements(SQL_FILE):
        if stmt.upper() in ("START TRANSACTION", "COMMIT") or stmt.upper().startswith(("SET SQL_MODE", "SET TIME_ZONE")):
            continue
        cur.execute(stmt)
        n += 1
    conn.commit()

    for t in ("foundation", "lipstick"):
        cur.execute(f"SELECT COUNT(*) FROM `{t}`")
        print(f"  {t}: {cur.fetchone()[0]} baris")
    print(f"Siap -- database '{db}' sedia ({n} statement dijalankan).")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
