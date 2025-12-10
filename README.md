# Earthquake Risk Detection Information System

## Overview
The **Earthquake Risk Detection Information System** is a data-driven engineering tool designed to help construction, civil, and industrial engineers make informed decisions using real-time seismic activity. The system integrates with the **USGS Earthquake API** to ingest live earthquake data, store it in a structured SQL database, and deliver analytical insights through a responsive Streamlit dashboard.

---

## Target Users

### Primary Users
- Construction engineers (infrastructure planning, seismic safety)

### Secondary Users
- Civil engineers (site analysis, hazard assessments)

### Tertiary Users
- Industrial engineers (disaster logistics, supply chain resilience)

---

## Primary Use Cases
- **Emergency Response Planning** – Identify optimal evacuation routes and resource allocation zones before and after seismic events.
- **Infrastructure Safety Evaluation** – Assess construction site viability using up-to-date seismic risk information.
- **Regional Seismic Risk Analysis** – Determine earthquake frequency, magnitude trends, and regional danger levels.

---

## System Architecture
[USGS API]
        ↓
[Backend: FastAPI + SQLModel]
        ↓
[SQLite Database]
        ↓
[Frontend: Streamlit Dashboard]


---

## Entity Relationships
- **Location (1 → many) Earthquake**
- **Earthquake (1 → many) Aftershock**

---

## Project Structure
```

backend/
├── database.py      # SQLite engine and table creation
├── models.py        # SQLModel ORM definitions
├── queries.py       # Database query logic
├── fetch_data.py    # API ingestion and database population
└── main.py          # FastAPI app and endpoints

frontend/
└── app.py           # Streamlit dashboard

requirements.txt      # Python dependencies
README.md             # Project documentation

```

---

## Technology Stack
- **Backend:** FastAPI, SQLModel, requests/httpx  
- **Database:** SQLite  
- **Frontend:** Streamlit  
- **Visualization:** Matplotlib  

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com//earthquake-risk-detection.git
cd earthquake-risk-detection

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/earthquake-risk-detection.git
cd earthquake-risk-detection
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database

```bash
python backend/database.py
```

### 4. Fetch Real-Time Data from USGS

```bash
python -m backend.fetch_data
```

### 5. Run the Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

API documentation available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 6. Run the Frontend Dashboard

```bash
cd frontend
streamlit run app.py
```

Dashboard available at: [http://localhost:8501](http://localhost:8501)

---

## API Endpoints

| Endpoint                                | Method | Description                                          |
| --------------------------------------- | -----: | ---------------------------------------------------- |
| `/earthquakes/nearby-aftershocks`       |    GET | Earthquakes with aftershocks within a radius         |
| `/regions/top-5-avg-magnitude`          |    GET | Top 5 regions by average magnitude                   |
| `/aftershocks/strong-24h`               |    GET | Aftershocks > 4.0 magnitude in last 24 hours         |
| `/aftershocks/main-info-magnitude-gt-5` |    GET | Aftershocks where main earthquake magnitude > 5      |
| `/regions/above-average-count`          |    GET | Regions with above-average earthquake counts         |
| `/regions/top-seismic-activity`         |    GET | Top 10 most seismically active regions               |
| `/earthquakes/above-average-magnitude`  |    GET | Earthquakes above overall average magnitude          |
| `/earthquakes/with-aftershocks-region`  |    GET | Earthquakes joined with region and aftershock info   |
| `/earthquakes/aftershock-counts`        |    GET | Aftershock counts per earthquake                     |
| `/earthquakes/above-threshold`          |    GET | Earthquakes above a user-defined magnitude threshold |
