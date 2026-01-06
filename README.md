# 🌦️ Weather Analyzer — Automated Data Pipeline

A production-ready **weather data pipeline** that fetches live weather data, stores it in PostgreSQL, performs analytics, and generates temperature trend visualizations automatically or on a schedule.

---

## 🔧 Features

- Fetches real-time weather data from OpenWeather API  
- Idempotent insertion into PostgreSQL  
- Historical data tracking with timestamps  
- Automated scheduling (cron-like)  
- Analytics: min / max / average temperatures  
- Trend visualization using matplotlib  
- Dockerized for local & CI/CD deployment  
- GitHub Actions → Docker Hub image publishing  
- Unit-tested core logic (pytest)

---

## 🧱 Tech Stack

- **Python 3.11**
- **PostgreSQL**
- **pandas / matplotlib**
- **schedule**
- **Docker / Docker Compose**
- **pytest**
- **GitHub Actions (CI/CD)**

---

## ⚙️ Setup

### 1️⃣ Create virtual environment
```
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate     # Windows
```

### 2️⃣ Install dependencies 
```
pip install -r requirements.txt
```

### 3️⃣ Environment variables (.env)
```
OPENWEATHER_API_KEY=your_api_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_db
DB_USER=user
DB_PASSWORD=pass
```

### ▶️ Run Commands
####🔹One-off pipeline (manual run)
```
python -m weather_analyzer.main \
  --cities Stockholm London "New York" \
  --raw-output data/history/raw
```
What it does:
- Fetches weather data
- Inserts into PostgreSQL
- Saves optional raw JSON snapshots

####🔹 Automated scheduler
```
python -m weather_analyzer.scheduler
```
What it does:
- Runs at scheduled time
- Fetches weather data
- Stores into PostgreSQL
- Computes analytics
- Generates plots automatically
Outputs:
- plots/temperature.png
- plots/temperature_trends_<city>.png

####🔹 Run analytics & plotting manually
```
python -m weather_analyzer.plotting.plot_trends_postgres
```

#### 🔹 Run tests
```
pytest
```
With coverage:
```
pytest --cov=weather_analyzer
```

## 🐳 Docker 
#### Build image:
```
docker build -t homams/weather_analyzer:latest .
```
#### Run with PostgreSQL:
```
docker-compose up --build
```

## CI/CD
- GitHub Actions builds Docker image
- Pushes automatically to Docker Hub:
```
homams/weather_analyzer:latest
```
Secrets required:
-
```
DOCKER_USERNAME
```
-
```
DOCKERHUB_TOKEN
```



