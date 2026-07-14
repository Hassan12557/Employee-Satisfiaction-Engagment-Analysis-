# EngageIQ — Predictive Workforce Analytics Engine

A production-grade, containerized Machine Learning application that leverages a Random Forest Regressor to predict employee satisfaction and identify key drivers of workplace engagement. Built on a full-stack Django framework, fully Dockerized, and optimized to run inside a resource-constrained production cloud environment.

## 🚀 Live Demo
Access the live application here: **[engageiqanalytics-yl1isepm.b4a.run](https://engageiqanalytics-yl1isepm.b4a.run)**

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
