# STARTUP GUIDE

## 1. Prerequisites
- **Python 3.x**
- **Node.js**
- **Mosquitto** (optional but recommended for Full IoT Mode)
- **Node-RED** (optional but recommended for Full IoT Mode)

## 2. Fast Demo Mode (Simulation)
If you cannot start Mosquitto or Node-RED, the project is designed to fallback to **SIMULATION MODE**.
1. Open Terminal 1:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
2. Open Terminal 2:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Open Dashboard at `http://localhost:5173`.
4. Click `SIMULATE IoT SENSOR DATA` to generate readings directly!

## 3. Full IoT Mode Demonstration
1. **Start Mosquitto** (`localhost:1883` should be running).
2. **Start Node-RED** (`node-red` in terminal).
   - Go to `http://localhost:1880`.
   - Import `nodered/flows.json`.
3. **Start Flask Backend** (`python app.py`).
4. **Start ESP32 Simulator** (`python iot_simulator.py` in a new terminal inside `backend/`).
5. **Start React Frontend** (`npm run dev`).
6. Open `http://localhost:5173`. The system will receive data via MQTT -> Node-RED -> Flask!
