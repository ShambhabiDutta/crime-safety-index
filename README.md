# Crime Safety Index System

## Overview

This project builds a geospatial crime analytics system that:

- Visualizes crime density using an interactive heatmap
- Computes a neighborhood-level Safety Index (0–100)
- Incorporates distance to nearest police station
- Exposes safety data via a REST API

The system uses Washington, DC crime data and official police station coordinates.

---

## Features

- 🔥 Crime heatmap visualization
- 🚓 Police station overlay
- 📊 Weighted crime severity model
- 📍 Distance-based safety modifier
- 🏙 Area-level safety ranking
- 🌐 REST API endpoints

---

## Safety Index Methodology

The safety score is computed using:

1. Crime severity weighting  
   - Violent crimes: weight = 5  
   - Property crimes: weight = 2  

2. Distance to nearest police station (Haversine formula)

3. Incident risk formula:

4. Area-level aggregation
5. Min-max normalization to 0–100 scale

Higher score = safer area.

---

## API Endpoints

### Home
Interactive heatmap with police stations.

### All Safety Scores
Returns JSON of all neighborhood safety scores.

### Individual Cluster

Example:

---

## Tech Stack

- Python
- Flask
- Pandas
- NumPy
- Folium

---

## How to Run

```bash
git clone <repo-url>
cd crime-safety-index
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python app.py
http://127.0.0.1:5000/
