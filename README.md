# 📈 Market chart

FastAPI backend for scraping, storing and serving Vietnamese gold price data (from PNJ and others).

---

## 🚀 Features

- Scheduled scraping from [giavang.pnj.com.vn](https://giavang.pnj.com.vn)
- Store prices in PostgreSQL
- JSON API:
  - `/gold-prices/live` – current prices
  - `/gold-prices/by-date?date=YYYY-MM-DD` – historical daily
  - `/gold-prices/range?start=YYYY-MM-DD&end=YYYY-MM-DD` – by range

---

## 🛠 Requirements

- Python 3.10+
- Docker & Docker Compose (for PostgreSQL)

---

## 🔧 Setup

### 1. Clone

git clone https://github.com/katsu-nt/market-chart.git
cd market-chart

### 2. Setup virtual env

python -m venv .venv
source .venv/bin/activate      # On Unix/macOS
.venv\Scripts\activate         # On Windows
pip install -r requirements.txt

### 3. Create .env file

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=data-chart
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

### 4. Start PostgreSQL

docker-compose up -d

### 5. Run server

uvicorn app.main:app --reload
