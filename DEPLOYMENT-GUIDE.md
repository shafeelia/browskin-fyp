# 🚀 Panduan Lengkap Deployment Sistem BrownSkin FYP

Dokumentasi ini menerangkan seni bina awan (*cloud architecture*), langkah-langkah *deployment*, konfigurasi pembolehubah persekitaran (*environment variables*), dan strategi pemantauan untuk sistem **BrownSkin** (Sistem Pengesanan Undertone & Cadangan Kosmetik Berasaskan AI).

---

## 1. Seni Bina Sistem (Architecture Overview)

Sistem BrownSkin menggunakan seni bina moden tanpa kos (100% Free-tier Cloud Architecture) yang bersedia untuk kegunaan produksi dan pembentangan Projek Tahun Akhir (FYP):

```
                      +-----------------------------+
                      |   Pengguna (Telefon / PC)   |
                      +--------------+--------------+
                                     |
                               HTTPS | (Kamera / Muat Naik Gambar)
                                     v
                      +-----------------------------+
                      |   Render.com (Web Service)  |
                      |  - Frontend: HTML/CSS/JS    |
                      |  - Backend: Flask + Gunicorn|
                      |  - ML: OpenCV + Scikit-Learn|
                      +--------------+--------------+
                                     |
                          MySQL+TLS  | Port 4000 (Query Shade & Gincu)
                                     v
                      +-----------------------------+
                      |    TiDB Cloud Serverless    |
                      |    (AWS Singapore Region)   |
                      | - Jadual: foundation (26)   |
                      | - Jadual: lipstick (21)     |
                      +-----------------------------+
                                     ^
                                     | HTTP Ping (Setiap 5 minit)
                      +--------------+--------------+
                      |         UptimeRobot         |
                      |    (Elak Server "Tidur")    |
                      +-----------------------------+
```

### Komponen Utama:
1. **Frontend**: Antaramuka web responsif (HTML5, Vanilla CSS, JS) yang menyokong kamera hadapan telefon pintar dan muat naik gambar.
2. **Backend**: Python Flask menggunakan pelayan produksi **Gunicorn**.
3. **Model AI**: 
   - **OpenCV (Haar Cascade)**: Mengecam kedudukan muka dan memotong zon pipi kiri & kanan secara automatik.
   - **Scikit-Learn (k-NN)**: Mengklasifikasikan undertone (*cool, neutral, warm, olive*) dan mengira skor keyakinan (*confidence rate*).
4. **Pangkalan Data (Database)**: **TiDB Cloud (Serverless MySQL)** berpusat di AWS Singapore dengan penyulitan TLS/SSL.
5. **Keep-Alive Monitor**: **UptimeRobot** menghantar isyarat `HTTP GET` setiap 5 minit untuk memastikan servis Render sentiasa aktif tanpa henti.

---

## 2. Langkah Demi Langkah Deployment

### Bahagian A: Pangkalan Data Awan (TiDB Cloud)
1. Buka [tidbcloud.com](https://tidbcloud.com) dan log masuk.
2. Cipta kluster baharu:
   - **Plan:** *Starter ($0/month, Free)*.
   - **Instance Name:** `brownskin-db`.
   - **Region:** *AWS Singapore (`ap-southeast-1`)*.
3. Dapatkan maklumat sambungan dari butang **Connect**:
   - **Host:** `gateway01.ap-southeast-1.prod.aws.tidbcloud.com`
   - **Port:** `4000`
   - **User:** `2cPx11MtXzY5S1d.root`
   - **Password:** *(Kata laluan yang dijana)*
4. Skrip pangkalan data (`undertone_detection.sql`) telah dimigrasikan ke dalam pangkalan data bernama `brownskin` yang mengandungi:
   - Jadual `foundation` (26 rekod padanan tona).
   - Jadual `lipstick` (21 rekod padanan gincu).

---

### Bahagian B: Hos Web & API (Render.com)
1. Buka [dashboard.render.com](https://dashboard.render.com) dan log masuk dengan GitHub.
2. Tekan butang **New +** ➡️ **Web Service**.
3. Pilih repository GitHub: `shafeelia/browskin-fyp`.
4. Masukkan konfigurasi berikut:
   - **Name:** `browskin-fyp`
   - **Language:** `Python 3`
   - **Branch:** `main`
   - **Region:** `Singapore (Southeast Asia)` (atau `Oregon (US West)`)
   - **Root Directory:** *(Biarkan kosong)*
   - **Build Command:**
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command:**
     ```bash
     cd backend && gunicorn -b 0.0.0.0:$PORT app:app
     ```
   - **Instance Type:** Pilih **Free ($0/month)**.

5. Tambah **Environment Variables** berikut di bahagian tetapan:
   | Key | Value | Catatan |
   | :--- | :--- | :--- |
   | `BROWNSKIN_DB_HOST` | `gateway01.ap-southeast-1.prod.aws.tidbcloud.com` | Host TiDB Cloud |
   | `BROWNSKIN_DB_PORT` | `4000` | Port TiDB |
   | `BROWNSKIN_DB_USER` | `2cPx11MtXzY5S1d.root` | Username TiDB |
   | `BROWNSKIN_DB_PASSWORD` | `EmwXfDbPFc1vK8WL` | Password database |
   | `BROWNSKIN_DB_NAME` | `brownskin` | Nama database |
   | `PYTHON_VERSION` | `3.12.0` | Versi Python |

6. Tekan butang **"Deploy web service"**.
7. Selepas proses binaan selesai, status akan bertukar menjadi **"Live"** dengan URL rasmi:
   👉 **`https://browskin-fyp.onrender.com`**

---

### Bahagian C: Memastikan Servis Sentiasa Aktif (UptimeRobot)
Pelayan percuma Render akan tidur (*spin-down*) secara automatik sekiranya tiada trafik melebihi 15 minit. UptimeRobot digunakan untuk menyelesaikan isu ini:

1. Daftar akaun percuma di [uptimerobot.com](https://uptimerobot.com).
2. Tekan **"+ Add New Monitor"**.
3. Tetapkan parameter berikut:
   - **Monitor Type:** `HTTP(s)`
   - **Friendly Name:** `BrownSkin Web Service`
   - **URL (or IP):** `https://browskin-fyp.onrender.com`
   - **Monitoring Interval:** `Every 5 minutes`
   - **Monitor Timeout:** `30 seconds`
4. Tekan **"Create Monitor"**.
5. Sistem kini akan aktif 24 jam sehari tanpa berlaku *cold start* yang lama.

---

## 3. Privasi Data & Pengendalian Imej (Security & Privacy)

Sistem ini direka khas mengikut amalan terbaik perlindungan privasi data:
- **Tiada Storan Imej Kekal**: Gambar muka pengguna yang dimuat naik atau ditangkap melalui kamera telefon **TIDAK DISIMPAN** ke dalam cakera keras (*hard drive*) pelayan mahupun pangkalan data.
- **Pemprosesan Dalam Memori Sahaja (RAM Buffer)**: Imej hanya dibaca sementara dalam memori komputer menggunakan fungsi `cv2.imdecode()` untuk proses pengesanan koordinat pipi dan pengiraan nilai purata RGB.
- **Penyulitan Dalam Transit (Encryption in Transit)**: Semua komunikasi antara pelayar pengguna, pelayan Render, dan pangkalan data TiDB Cloud menggunakan protokol selamat **HTTPS** dan **TLS 1.2/1.3**.

---

## 4. Panduan Penyelesaian Masalah (Troubleshooting)

### A. Ralat Semasa Build: `libGL.so.1: cannot open shared object file`
- **Punca**: Pakej `opencv-python` standard memerlukan pustaka GUI Linux.
- **Penyelesaian**: Gunakan `opencv-python-headless` dalam `requirements.txt` (telah dikemaskini dalam sistem).

### B. Sambungan Database Gagal / Timeout
- Pastikan pembolehubah `BROWNSKIN_DB_PORT` ditetapkan kepada `4000` (bukan 3306).
- Pastikan sambungan menyokong SSL (`ssl_disabled=False` telah diintegrasikan dalam modul `db_utils.py`).

### C. Kamera Telefon Tidak Berfungsi
- Akses kamera pelayar web moden memerlukan sambungan **HTTPS** yang sah. Dengan menggunakan domain Render (`https://...`), fungsi kamera boleh terus diakses dengan selamat pada pelayar Chrome dan Safari telefon pintar.

---

*Disediakan untuk Projek Tahun Akhir (FYP) — BrownSkin Undertone Detection & Recommendation System.*
