# Node-RED Enabled Smart Energy Consumption Optimization Using Dynamic Programming

**Short Name:** SmartEnergy DP  
**Tagline:** Intelligent Energy Monitoring and Optimal Device Scheduling

## 1. Problem Statement
A smart building/home contains multiple electrical devices. The system must determine which devices should be operated and for how long to achieve the best possible energy utilization while respecting the available energy limit and device priorities.

## 2. Dynamic Programming Concept & Mathematical Formulation
The optimization uses a **0/1 Knapsack-style Dynamic Programming** algorithm.
- **Weight:** Device Energy Requirement (Power Watts)
- **Value:** Device Priority
- **Capacity (W):** Available Energy Budget

### Recurrence Relation:
```
if energy[i] <= w:
    dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-energy[i]])
else:
    dp[i][w] = dp[i-1][w]
```

### Complexity:
- **Time Complexity:** `O(n × W)`
- **Space Complexity:** `O(n × W)`
*(where n = number of devices, W = energy capacity)*

## 3. IoT Architecture & Node-RED Integration
**● DEMO / SIMULATION MODE:**
Sensor readings shown in this academic prototype are generated through a software simulation. 
This project integrates **Node-RED** as a powerful IoT gateway layer.

### Current System Architecture with Node-RED
```
ESP32 (MQTT Simulator) -> Node-RED (MQTT -> HTTP) -> Flask API -> SQLite / Pandas -> DP Optimizer -> React Dashboard
```

### Future Physical Integration
```
Energy Sensors -> Physical ESP32 -> Wi-Fi -> Node-RED Gateway -> Flask API -> SQLite -> DP Optimizer -> React Dashboard
```

## 4. Technologies Used
- **Frontend:** React, Vite, CSS, Node.js (Fetch API)
- **Backend:** Python, Flask, Flask-CORS, SQLite, Pandas, OpenPyXL
- **Database:** SQLite (`energy.db`) + Excel historical data (`Smart_Energy_Dataset.xlsx`)

## 5. API Endpoints
- `GET /api/devices`: List of configured IoT devices
- `GET /api/sensor-readings`: Live simulated sensor data
- `GET /api/energy-summary`: Aggregated power statistics
- `POST /api/simulate`: Trigger new simulated IoT reading
- `POST /api/optimize`: Execute DP algorithm with `{"energy_budget": 5000}`
- `GET /api/historical-analytics`: Analyzes the Pandas dataset

## 6. How to Run (Two-Terminal Architecture)

### Terminal 1 — Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*(Backend runs at http://127.0.0.1:5000)*

### Terminal 2 — Frontend
```bash
cd frontend
npm install
npm run dev
```
*(Frontend runs at http://localhost:5173)*

## 7. Viva Explanation / Demonstration Flow
1. **Dashboard Load:** Real-time metrics appear via SQLite.
2. **IoT Simulation:** Shows voltage, current, and power dynamically.
3. **Optimization:** Input a budget (e.g., 5000 Wh). Click Optimize.
4. **DP Processing:** Flask reads SQLite data, processes `O(n × W)` DP matrix, and backtracks to find the exact devices.
5. **Analytics:** Show historical cost and usage loaded via Pandas.

## 8. GitHub Instructions
To push to your own repository:
```bash
git init
git add .
git commit -m "Initial SmartEnergy DP implementation"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
