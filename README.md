## Project_1
NASA Near-Earth Object (NEO) Tracking &amp; Insights using Public API
# 🚀 NASA Near-Earth Object (NEO) Tracking & Insights

This project visualizes and analyzes Near-Earth Object (asteroid) data using NASA's public API and a MySQL database. It helps track asteroid approaches to Earth, identify potentially hazardous objects, and explore trends using an interactive Streamlit web app.

## 🔍 Features

- Connects to NASA's NEO API to fetch asteroid data (ID, size, velocity, distance, hazard status, etc.).
- Stores data in a structured MySQL database with two tables: `asteroids` and `close_approach`.
- Provides pre-built analytical queries to gain insights such as:
  - Fastest, slowest, and largest asteroids
  - Hazardous asteroid detection
  - Frequency of close approaches
  - Asteroids passing closer than the Moon
- Includes filters on key attributes (date, velocity, size, hazard status, etc.).
- Interactive Streamlit dashboard for:
  - Query selection
  - Data filtering
- Sidebar navigation to switch between "Queries" and "Filters".

## 🛠️ Technologies Used

- **Python**
- **Streamlit** (frontend dashboard)
- **MySQL** (database storage)
- **NASA Open API** (data source)
- **Pandas** (data handling)

## 📆 Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install streamlit pymysql requests pandas
   ```
3. Configure MySQL database (create `asteroid` database and required tables).
4. Run the app:
   ```bash
   streamlit run astro.py
   ```

## 🔑 API Key

You need a NASA API key to access the data. You can get a free one from:\
[https://api.nasa.gov/](https://api.nasa.gov/)

## 📊 Example Queries

- List top 10 fastest asteroids
- Find potentially hazardous asteroids with more than 3 approaches
- Count of asteroid approaches per month
- Closest ever asteroid approaches
- Asteroids with diameter > 1 km

## 📁 Database Schema

- **asteroids**: ID, name, magnitude, diameter (min/max), hazard status
- **close\_approach**: Neo ID, date, velocity, astronomical (AU), miss distance (km/LD), orbiting body

## 🚁 Data Source

All asteroid data is retrieved from NASA's [NeoWs API](https://api.nasa.gov/).

