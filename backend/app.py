from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection, init_db
from dp_optimizer import optimize_energy
from simulator import generate_sensor_data
from analytics import get_historical_analytics
import json
import os
import threading
import paho.mqtt.client as mqtt
from datetime import datetime

app = Flask(__name__)
CORS(app)

init_db()

# --- MQTT SETUP ---
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "smartenergy/dp/sensors"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT Broker ({MQTT_BROKER}) with code {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"\n[MQTT RECEIVED] Topic: {msg.topic} | Payload: {payload}")
        data = json.loads(payload)
        
        # Save to database
        conn = get_db_connection()
        c = conn.cursor()
        
        device_id = data.get('device_id')
        voltage = data.get('voltage', 230)
        current = data.get('current', 0)
        power = data.get('power', 0)
        energy_kwh = data.get('energy_kwh', 0)
        temp = data.get('temperature', 25.0)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute('''
            INSERT INTO sensor_readings (device_id, timestamp, voltage, current, power, energy_kwh, temperature)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (device_id, timestamp, voltage, current, power, energy_kwh, temp))
        conn.commit()
        conn.close()
        print(f"[DB] Saved MQTT sensor data for {device_id}")
    except Exception as e:
        print(f"[MQTT ERROR] Failed to process message: {e}")

def start_mqtt():
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")

# Start MQTT client in background
start_mqtt()
# ------------------


@app.route('/')
def index():
    return jsonify({"message": "SmartEnergy DP API", "mode": "Simulation"})

@app.route('/dashboard')
def dashboard():
    return jsonify({"message": "Use the React frontend for the dashboard."})

@app.route('/api/devices', methods=['GET'])
def get_devices():
    conn = get_db_connection()
    devices = conn.execute('SELECT * FROM devices').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in devices])

@app.route('/api/device/<device_id>', methods=['GET'])
def get_device(device_id):
    conn = get_db_connection()
    device = conn.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,)).fetchone()
    conn.close()
    if device:
        return jsonify(dict(device))
    return jsonify({"error": "Not found"}), 404

@app.route('/api/sensor-readings', methods=['GET'])
def get_sensor_readings():
    conn = get_db_connection()
    query = '''
        SELECT s.*, d.device_name 
        FROM sensor_readings s
        JOIN devices d ON s.device_id = d.device_id
        WHERE s.id IN (
            SELECT MAX(id) FROM sensor_readings GROUP BY device_id
        )
    '''
    readings = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in readings])

@app.route('/api/energy-summary', methods=['GET'])
def get_energy_summary():
    conn = get_db_connection()
    total_devices = conn.execute('SELECT COUNT(*) FROM devices').fetchone()[0]
    active_devices = conn.execute('SELECT COUNT(*) FROM devices WHERE status = "ACTIVE"').fetchone()[0]
    total_power = conn.execute('SELECT SUM(power_watts) FROM devices WHERE status = "ACTIVE"').fetchone()[0] or 0
    today_energy = conn.execute('SELECT SUM(energy_consumption) FROM devices').fetchone()[0] or 0
    
    # Calculate peak from sensor_readings
    peak_power = conn.execute('SELECT MAX(power) FROM sensor_readings').fetchone()[0] or total_power
    avg_power = conn.execute('SELECT AVG(power) FROM sensor_readings WHERE power > 0').fetchone()[0] or total_power
    
    conn.close()
    
    return jsonify({
        "total_devices": total_devices,
        "active_devices": active_devices,
        "total_power": total_power,
        "today_energy": today_energy,
        "estimated_cost": round((today_energy / 1000) * 0.15, 2),
        "peak_power": peak_power,
        "average_power": round(avg_power, 2)
    })

@app.route('/api/simulate', methods=['POST'])
def simulate():
    readings = generate_sensor_data()
    return jsonify({"success": True, "readings": readings})

@app.route('/api/optimize', methods=['POST'])
def optimize():
    data = request.json
    budget = data.get('energy_budget', 5000)
    result = optimize_energy(budget)
    return jsonify({"success": True, **result})

@app.route('/api/optimization-history', methods=['GET'])
def get_optimization_history():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM optimization_results ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()
    
    res = []
    for h in history:
        d = dict(h)
        d['devices_selected'] = json.loads(d['devices_selected'])
        res.append(d)
        
    return jsonify(res)

@app.route('/api/historical-analytics', methods=['GET'])
def historical_analytics():
    return jsonify(get_historical_analytics())

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    # This endpoint receives data from Node-RED
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
        
    conn = get_db_connection()
    c = conn.cursor()
    
    device_id = data.get('device_id')
    voltage = data.get('voltage', 230)
    current = data.get('current', 0)
    power = data.get('power', 0)
    energy_kwh = data.get('energy_kwh', 0)
    temp = data.get('temperature', 25.0)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute('''
        INSERT INTO sensor_readings (device_id, timestamp, voltage, current, power, energy_kwh, temperature)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (device_id, timestamp, voltage, current, power, energy_kwh, temp))
    c.execute('''
        INSERT INTO events (device_id, event_type, message, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (device_id, 'MQTT_DATA', f"Data received via Node-RED ({power} W)", timestamp))
    
    conn.commit()
    conn.close()
    
    print(f"[Node-RED -> Flask] Saved sensor data for {device_id}")
    return jsonify({"success": True, "message": "Data saved successfully"})

@app.route('/api/search', methods=['GET'])
def search_devices():
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    c = conn.cursor()
    # Search in devices table
    devices = c.execute('SELECT * FROM devices WHERE lower(device_id) LIKE ? OR lower(device_name) LIKE ? OR lower(status) LIKE ? OR lower(location) LIKE ?', 
                        (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
    
    results = []
    for d in devices:
        dev = dict(d)
        latest_sensor = c.execute('SELECT * FROM sensor_readings WHERE device_id = ? ORDER BY id DESC LIMIT 1', (dev['device_id'],)).fetchone()
        if latest_sensor:
            dev.update(dict(latest_sensor))
        results.append(dev)
    conn.close()
    return jsonify(results)

@app.route('/api/recent-events', methods=['GET'])
def get_recent_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    return jsonify([dict(e) for e in events])

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
