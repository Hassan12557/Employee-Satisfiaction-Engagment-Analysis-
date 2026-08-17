# EngageIQ — Predictive Workforce Analytics Engine

A production-grade, containerized Machine Learning application that leverages a Random Forest Regressor to predict employee satisfaction and identify key drivers of workplace engagement. Built on a full-stack Django framework, fully Dockerized, and optimized to run inside a resource-constrained production cloud environment.

## 🚀 Live Demo
Access the live application here: 

https://engageiqanalytics-bmi22uh7.b4a.run/
---

## 🏗️ End-to-End System Architecture

This project bridges the gap between machine learning model exploration and full-stack software deployment. The complete pipeline is structured as follows:
[Raw Workplace Data]
│
▼
[Data Preprocessing & Feature Engineering] (Pandas, Scikit-Learn)
│
▼
[Random Forest Training & Serialization] (Generating satisfaction_regressor.pkl)
│
▼
[Django REST API & Web UI Layer] (Predictive endpoints & CSS dark UI)
│
▼
[Docker Containerization] (Isolating system files & local database)
│
▼
[Production RAM Optimization] (Memory profiling & server run-tweaks)
---

## 🛠️ Technology Stack

* **Machine Learning:** Python, Scikit-Learn (Random Forest Regressor), Pandas, NumPy, Pickle
* **Web & API Framework:** Django 5.2, Django REST Framework
* **Containerization & DevOps:** Docker, Docker Compose
* **Database:** SQLite (local persistent schemas)
* **Hosting & Infrastructure:** Back4app Containers (Serverless micro-VMs)
* **Development Environment:** GitHub Codespaces (Linux)

---

## 🔧 Deep Dive: Pipeline Phases

### 1. Data Preprocessing & Feature Engineering
* Handled workplace feature scaling, missing variable imputations, and structural mappings.
* Managed categorical variables (such as departments or experience levels) using clean encoding pipelines.

### 2. Model Training & Serialization
* Trained a high-accuracy **Random Forest Regressor** to predict employee job satisfaction indexes.
* Serialized the finalized model state to `satisfaction_regressor.pkl` to allow high-speed offline inference without retraining the model on every incoming web request.

### 3. REST API & Web Dashboard Development
* Developed a high-performance endpoint (`/api/predict-satisfaction/`) that handles POST requests with JSON payloads, converts input parameters into a tabular DataFrame format, runs inference, and delivers predicted metrics instantly.
* Developed and styled a premium, dark-themed corporate landing page demonstrating live pipeline streams.

### 4. Dockerization & Resource Optimization
* Constructed a robust, multi-layered `Dockerfile` using `python:3.11-slim` to minimize the image footprint and enforce environmental parity.
* **The 256MB RAM Hack:** To deploy on a free cloud tier with strict memory limits, Django’s development auto-reloader was disabled using the `--noreload` flag. This single optimization cut the application’s operating RAM footprint in half, preventing Out-of-Memory (OOM) server crashes!

here is snapshots
 <img width="1344" height="643" alt="1" src="https://github.com/user-attachments/assets/9d8593b2-652a-4423-9d1c-585af117caf6" />
 <img width="1287" height="615" alt="Capture6" src="https://github.com/user-attachments/assets/f66bcae2-3112-487e-91c1-cd8418874059" />
<img width="1266" height="510" alt="10" src="https://github.com/user-attachments/assets/344523e1-6880-4239-b9e8-da26bbee471e" />
<img width="1332" height="620" alt="8" src="https://github.com/user-attachments/assets/05cb8beb-8e3b-4a8b-a840-bd57daae1f34" />
<img width="1340" height="595" alt="7" src="https://github.com/user-attachments/assets/9be4f9af-725d-4e6b-adbe-4a53c1f8f689" />
<img width="1289" height="625" alt="5" src="https://github.com/user-attachments/assets/7c795478-06b4-4b4a-b048-bc1a08ed3579" />
<img width="1314" height="634" alt="4" src="https://github.com/user-attachments/assets/ec859ca8-a27a-467f-8004-6f64f01b5e39" />
<img width="1314" height="567" alt="3" src="https://github.com/user-attachments/assets/147a74dd-5549-4571-a044-d67812a29700" />
<img width="1255" height="529" alt="2" src="https://github.com/user-attachments/assets/8656287e-f606-405f-8ac6-6293153598d9" />
<img width="1281" height="596" alt="image" src="https://github.com/user-attachments/assets/1669156e-1cdf-4a99-b8b2-eeaac37a6ac0" />

---

## 💻 Local Setup & Installation

To run this application locally on your machine, ensure you have **Docker** installed, and execute the following commands in your terminal:

### 1. Clone the Repository
```bash
git clone [https://github.com/Hassan12557/Employee-Satisfiaction-Engagment-Analysis-.git](https://github.com/Hassan12557/Employee-Satisfiaction-Engagment-Analysis-.git)
cd Employee-Satisfiaction-Engagment-Analysis-/engageiq_web
│
▼
[Continuous Cloud Deployment] (Git-triggered CI/CD to Back4app)
2. Build the Docker Image
To bypass any cached build layers and copy all database/model resources fresh, run:
Run the Container
Spin up the container and map internal port 8000 to your host machine:

Bash
docker run -p 8000:8000 engageiq-app
Once initialized, navigate to http://localhost:8000/ in your browser to explore the dashboard.

💡 Key Engineering Wins
Environment Independence: Achieved zero variance between local development and cloud production configurations.

Low-Footprint Design: Handled strict hardware constraints by removing local python compiler overhead and managing caching during build stages.

Stateless Portability: Designed self-healing Django database migration pathways that execute cleanly upon container launch.
