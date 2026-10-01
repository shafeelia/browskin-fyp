# Cloud Deployment and System Architecture Guide: BrownSkin FYP

This document outlines the cloud infrastructure, deployment procedures, environment variable configurations, and monitoring strategies for the **BrownSkin** system (AI-Powered Undertone Detection and Cosmetic Recommendation System).

---

## 1. System Architecture Overview

The BrownSkin system utilizes a zero-cost, production-ready cloud architecture (100% Free-Tier) optimized for low latency, secure data handling, and high availability:

```
                      +-----------------------------+
                      |   Client (Mobile / Desktop) |
                      +--------------+--------------+
                                     |
                               HTTPS | (Camera Stream / Image Upload)
                                     v
                      +-----------------------------+
                      |   Render.com (Web Service)  |
                      |  - Frontend: HTML5/CSS3/JS  |
                      |  - Backend: Flask + Gunicorn|
                      |  - ML Engine: OpenCV + k-NN |
                      +--------------+--------------+
                                     |
                           MySQL+TLS | Port 4000 (Query Shade & Lipstick)
                                     v
                      +-----------------------------+
                      |    TiDB Cloud Serverless    |
                      |    (AWS Singapore Region)   |
                      | - Table: foundation (26)    |
                      | - Table: lipstick (21)      |
                      +-----------------------------+
                                     ^
                                     | HTTP Ping (Every 5 minutes)
                      +--------------+--------------+
                      |         UptimeRobot         |
                      |    (Prevents Cold Start)    |
                      +-----------------------------+
```

### Core Architecture Layers:

1. **Presentation Layer (View / Frontend)**:
   - Responsive web interface built with standard HTML5, CSS3, and JavaScript.
   - Supports mobile front-facing camera streaming via HTML5 `MediaDevices.getUserMedia()` and manual file uploads.

2. **Application Layer (Controller & Server)**:
   - Python 3.12 Flask framework managed by the **Gunicorn WSGI** production server.
   - Modular MVC structure separating route controllers (`predict_controller.py`) from database models (`db_models.py`).

3. **Machine Learning Pipeline (Model)**:
   - **OpenCV (Haar Cascade)**: Automatically locates facial bounds and isolates cheek regions (left and right) to minimize background noise.
   - **Normalized Chromaticity Extraction**: Computes normalized $r, g, b$ color ratios to insulate predictions from varying ambient lighting conditions.
   - **Scikit-Learn (k-Nearest Neighbors & StandardScaler)**: Classifies user undertones into *cool, neutral, warm, or olive* categories and computes sample-specific confidence ratings.

4. **Persistence Layer (Database Model)**:
   - **TiDB Cloud Serverless (MySQL Compatible)** hosted in AWS Singapore (`ap-southeast-1`).
   - Secure TLS/SSL encrypted connection on port 4000.
   - Contains cosmetic shade tables (`foundation` with 26 records, `lipstick` with 21 records).

5. **High Availability Monitoring**:
   - **UptimeRobot** issues an HTTP GET ping every 5 minutes to prevent Render free-tier instances from entering idle sleep mode.

---

## 2. Step-by-Step Deployment Procedure

### Part A: Cloud Database Setup (TiDB Cloud)

1. Sign in to [tidbcloud.com](https://tidbcloud.com).
2. Create a serverless cluster:
   - **Plan**: Starter ($0/month, Free).
   - **Cluster / Instance Name**: `brownskin-db`.
   - **Region**: AWS Singapore (`ap-southeast-1`).
3. Retrieve connection parameters via the **Connect** modal:
   - **Host**: `gateway01.ap-southeast-1.prod.aws.tidbcloud.com`
   - **Port**: `4000`
   - **User**: `2cPx11MtXzY5S1d.root`
   - **Password**: *(Generated authentication secret)*
4. The database schema from `database/undertone_detection.sql` is migrated to the `brownskin` database, containing:
   - Table `foundation`: maps undertone and skintone combinations to foundation product names.
   - Table `lipstick`: maps undertone and skintone combinations to lipstick product names.

---

### Part B: Web Service Hosting (Render.com)

1. Sign in to [dashboard.render.com](https://dashboard.render.com) using GitHub.
2. Select **New +** > **Web Service**.
3. Link the repository: `shafeelia/browskin-fyp`.
4. Configure service specifications:
   - **Name**: `browskin-fyp`
   - **Language**: `Python 3`
   - **Branch**: `main`
   - **Region**: `Singapore (Southeast Asia)` (or `Oregon (US West)`)
   - **Root Directory**: *(Leave blank)*
   - **Build Command**:
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command**:
     ```bash
     cd backend && gunicorn -b 0.0.0.0:$PORT app:app
     ```
   - **Instance Type**: Select **Free ($0/month)**.

5. Configure **Environment Variables** in the service dashboard:

| Variable Key | Assigned Value | Description |
| :--- | :--- | :--- |
| `BROWNSKIN_DB_HOST` | `gateway01.ap-southeast-1.prod.aws.tidbcloud.com` | TiDB Cloud Gateway Host |
| `BROWNSKIN_DB_PORT` | `4000` | TiDB Public Port |
| `BROWNSKIN_DB_USER` | `2cPx11MtXzY5S1d.root` | TiDB Authentication Username |
| `BROWNSKIN_DB_PASSWORD` | `EmwXfDbPFc1vK8WL` | TiDB Authentication Password |
| `BROWNSKIN_DB_NAME` | `brownskin` | Target Database Name |
| `PYTHON_VERSION` | `3.12.0` | Python Runtime Version |

6. Click **Deploy Web Service**.
7. Once the build completes, the application URL will be live at:
   `https://browskin-fyp.onrender.com`

---

### Part C: Service Availability Monitoring (UptimeRobot)

Free instances on Render spin down after 15 minutes of inactivity. UptimeRobot ensures continuous responsiveness:

1. Register an account at [uptimerobot.com](https://uptimerobot.com).
2. Click **+ Add New Monitor**.
3. Set the following monitor fields:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `BrownSkin Web Service`
   - **URL (or IP)**: `https://browskin-fyp.onrender.com`
   - **Monitoring Interval**: `Every 5 minutes`
   - **Monitor Timeout**: `30 seconds`
4. Click **Create Monitor**.
5. The application remains warm in memory, eliminating cold-start latency for end users.

---

## 3. Data Privacy and Security Standards

1. **Transient In-Memory Processing**:
   - Uploaded user facial photographs are **never stored** on physical storage drives or persisted in the database.
   - Images are loaded into a temporary memory buffer (RAM) using `cv2.imdecode()`. Once facial color coordinates are extracted, the buffer is immediately purged.

2. **Transport Layer Security (TLS)**:
   - All client-to-server traffic is enforced over HTTPS via valid TLS certificates managed by Render.
   - Database queries between Flask and TiDB Cloud are encrypted using SSL/TLS protocols over port 4000.

3. **Secure Mobile Camera Access**:
   - Modern mobile operating systems (iOS and Android) require a valid HTTPS connection to grant web camera permissions. Deployment on Render provides automated HTTPS compliance, enabling direct camera capture in mobile browsers.

---

## 4. Technical Troubleshooting Guide

### Issue 1: Missing GUI Libraries During Linux Build (`libGL.so.1`)
- **Root Cause**: The default `opencv-python` package requires X11/GUI system libraries that are omitted in headless Linux cloud containers.
- **Resolution**: Install `opencv-python-headless` instead in `backend/requirements.txt`.

### Issue 2: TiDB Connection Refused or Authentication Failure
- Verify that `BROWNSKIN_DB_PORT` is explicitly set to `4000` rather than the default MySQL port `3306`.
- Ensure SSL configuration (`ssl_disabled=False`) is active within `db_models.py` when communicating with `tidbcloud.com`.

### Issue 3: Face Detection Failure on Submissions
- The Haar Cascade algorithm requires an unobstructed, forward-facing view of the facial structure under balanced lighting. If facial landmarks cannot be established, the API returns a structured HTTP 422 JSON message requesting a clearer image.

---

## 5. Repository File Structure

```text
BrownSkin_Combined/
|-- .gitignore
|-- CARA-GUNA.md
|-- DEPLOYMENT-GUIDE.md
|-- database/
|   |-- undertone_detection.sql
|   `-- setup_database.py
|-- ml_pipeline/
|   |-- dataset/
|   |-- test_images/
|   |-- data/
|   |   `-- undertone_features.csv
|   |-- training/
|   |   |-- train_knn.py
|   |   |-- train_model.py
|   |   |-- test_k_values.py
|   |   `-- predict.py
|   `-- utils/
|       `-- undertone_utils.py
|-- backend/
|   |-- app.py
|   |-- config.py
|   |-- requirements.txt
|   |-- models/
|   |   |-- saved_models/
|   |   |   |-- knn_model.pkl
|   |   |   `-- scaler.pkl
|   |   `-- db_models.py
|   |-- controllers/
|   |   `-- predict_controller.py
|   |-- utils/
|   `-- db_utils.py
`-- website/
    |-- pages/
    |   |-- home.html
    |   `-- test_upload.html
    |-- css/
    |   `-- style.css
    |-- js/
    |   `-- script.js
    `-- images/
        |-- banners/
        |-- products/
        `-- shades/
```
