# Cara Guna — BrownSkin (Undertone Detection)

## Apa yang saya baiki

1. **Ketepatan kiraan undertone** — ciri (features) yang digunakan untuk KNN
   ditukar daripada RGB/HSV mentah kepada *normalized chromaticity*
   (`rn`, `gn`, `bn` = nisbah R/G/B berbanding jumlah R+G+B). Diuji dengan
   5-fold cross-validation berulang (`test_k_values.py`), ciri ni beri
   accuracy purata **~66%**, berbanding **~52%** dengan ciri asal
   (R,G,B,H,S,V mentah) — sebab ia tak terjejas oleh kecerahan/lighting
   gambar, hanya nisbah warna (yang lebih berkait dengan undertone).
2. **Nilai k (n_neighbors)** kini dipilih **automatik** ikut
   cross-validation dalam `train_knn.py` (bukan `3` yang ditetapkan
   secara agak-agak) — sekarang k=9 (akan berubah sikit kalau dataset
   korang tambah/kurang gambar, sebab tu automatik).
3. **Model akhir** di-fit semula guna **SEMUA** 151 gambar dataset
   (bukan cuma 80%), supaya model produksi guna maklumat maksimum.
4. **Bug `Contact.html`** (huruf besar C) dibetulkan jadi `contact.html`
   — ni penting sebab server (Flask/Linux) *case-sensitive*, jadi
   sebelum ni link tu akan rosak (404) bila dibuka dari fon/server
   sebenar walaupun nampak OK kat laptop Windows.
5. **CSS mobile-safety** ditambah (imej auto-resize, elak scroll
   mendatar) supaya semua muka surat lagi selamat di skrin kecil.

⚠️ **Nota jujur**: dataset ni cuma 151 gambar untuk 4 kelas (cool/
neutral/olive/warm). Dengan data sebanyak ni, ~66-74% accuracy adalah
had praktikal yang munasabah untuk KNN — bukan sebab code ada bug, tapi
sebab tugasan (bezakan undertone dari warna kulit) memang sukar dan
dataset kecil. Nak naikkan accuracy dengan ketara, cara paling berkesan
ialah **tambah lebih banyak gambar dataset** (terutamanya untuk kelas
yang confuse antara satu sama lain — tengok `classification_report`
bila run `train_knn.py`).

## Macam mana nak tambah gambar dataset & retrain

1. Letak gambar baru dalam `backend/dataset/<cool|neutral|olive|warm>/`
2. Run:
   ```
   cd backend
   python train_model.py
   python train_knn.py
   ```
3. `knn_model.pkl` dan `scaler.pkl` akan update automatik.

## Cara jalankan server

```
cd backend
pip install -r requirements.txt
python app.py
```

Bila server start, terminal akan tunjuk 2 alamat:
```
Di laptop ni       : http://127.0.0.1:5000
Dari fon (WiFi sama): http://<IP-laptop>:5000
```

## Cara buka di laptop

Buka browser, pergi ke `http://127.0.0.1:5000`

## Cara buka di fon (paling penting untuk demo)

1. **Fon dan laptop MESTI sambung WiFi yang SAMA.**
2. Di laptop, run `python app.py` — tengok baris
   `Dari fon (WiFi sama): http://<IP-laptop>:5000` dalam terminal.
3. Di fon, buka browser (Chrome/Safari), taip alamat tu (contoh:
   `http://192.168.1.5:5000`).
4. Website akan terbuka macam biasa. Pergi ke halaman **Detect Skin**,
   tekan **"Open Front Camera"** — ni akan buka terus app kamera asal
   fon (bukan minta izin kamera dalam browser), so ia berfungsi walaupun
   guna `http://` (tak perlu HTTPS untuk cara ni).
5. Ambil gambar → tekan **Analyze Skin** → hasil akan terus dapat dari
   server di laptop korang.

### Kalau tak dapat sambung dari fon
- Pastikan **firewall Windows** tak sekat port 5000 (kalau perlu, benarkan
  "Python" bila Windows tanya "Allow this app through firewall").
- Pastikan laptop dan fon betul-betul dalam WiFi yang sama (bukan satu
  guna data mobile).
- Cuba buka `http://<IP-laptop>:5000` di browser laptop dulu untuk
  pastikan server jalan betul, baru cuba dari fon.

## Pangkalan data (MySQL/XAMPP)

## Seni Bina Projek (MVC Architecture)

Projek disusun mengikut corak **Model-View-Controller (MVC)** yang teratur:

```
BrownSkin_Combined/
├── backend/
│   ├── app.py                      # [ENTRY POINT] Inisialisasi Flask, pendaftaran Controllers (Blueprints)
│   ├── config.py                   # [CONFIG] Tetapan direktori, path model, & konfigurasi DB
│   │
│   ├── models/                     # [MODEL] Lapisan Logik Perniagaan & Data
│   │   ├── __init__.py
│   │   ├── undertone_model.py      # Pengecaman wajah, ekstraksi warna (rn,gn,bn), ramalan KNN & keyakinan
│   │   └── recommendation_model.py # Pertanyaan data MySQL bagi padanan produk foundation & lipstick
│   │
│   ├── controllers/                # [CONTROLLER] Lapisan Pengendalian Laluan & Permintaan
│   │   ├── __init__.py
│   │   ├── page_controller.py      # Laluan paparan (/ -> home.html, aset statik, /test-upload)
│   │   └── prediction_controller.py # Laluan API (POST /predict) - validasi, orkestrasikan Models, pulangkan JSON
│   │
│   ├── views/                      # [VIEW - Backend Reference]
│   │   └── __init__.py             # Merujuk kepada folder website/ sebagai View utama
│   │
│   ├── db_utils.py                 # Wrapper ke belakang untuk keserasian skrip lama
│   ├── undertone_utils.py          # Wrapper ke belakang untuk keserasian skrip lama
│   ├── setup_database.py           # Skrip inisialisasi pangkalan data
│   ├── train_model.py              # Ekstrak ciri dataset ke undertone_features.csv
│   ├── train_knn.py                # Latih model KNN dan simpan knn_model.pkl & scaler.pkl
│   └── test_k_values.py            # Ujian cross-validation nilai k
│
├── website/                        # [VIEW] Lapisan Paparan Pengguna (Frontend Presentation)
│   ├── home.html                   # Antara muka satu halaman (Home, Products, Detect Skin, Results)
│   ├── style.css                   # Gaya visual & susun atur
│   ├── script.js                   # Interaksi pelanggan, kamera, dan panggilan AJAX ke Controller
│   └── *.png                       # Aset grafik, ikon jenama, dan swatch produk
│
└── database/
    └── undertone_detection.sql     # Skrip bina jadual foundation & lipstick
```

### Pangkalan Data TiDB Cloud (Aktif Sekarang)

Projek kini dikonfigurasi terus menggunakan **TiDB Cloud** (tidak perlu lagi run XAMPP secara lokal):
- **Host**: `gateway01.ap-southeast-1.prod.aws.tidbcloud.com`
- **Port**: `4000`
- **User**: `2cPx11MtXzY5S1d.root`
- **Database**: `brownskin`
- **SSL**: Disokong automatik (TLS)

### Untuk Reset / Import Semula Data:
1. `cd backend`
2. `python setup_database.py` -> Membina semula jadual `foundation` (18 baris) & `lipstick` (36 baris) di TiDB Cloud.
3. `python app.py` -> Terminal akan memaparkan `Database : MySQL OK (foundation: 18 baris, lipstick: 36 baris)`.

## Nota website baru
- Banner utama kini guna `baru.png` (banner penuh lebar). Tukar nama fail dalam `home.html` kalau nak guna gambar lain.
- `website/` kini guna versi satu-page terbaru (`home.html`). Fail asal
  `scripe.js` dinamakan semula jadi `script.js` sebab `home.html` panggil `script.js`.
- Halaman lama (about/contact/detect/result/undertone .html) dibuang sebab dah
  digabung dalam `home.html`.
- Gambar lipstick: script.js cari `shade lipstick/<shade>.png`. Folder tu belum
  ada, jadi gambar lipstick guna gambar fallback sehingga korang tambah folder tu.
