import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'energy.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Devices table
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE,
            device_name TEXT,
            device_type TEXT,
            power_watts REAL,
            priority INTEGER,
            status TEXT,
            operating_hours REAL,
            energy_consumption REAL,
            location TEXT
        )
    ''')
    
    # Sensor Readings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            voltage REAL,
            current REAL,
            power REAL,
            energy_kwh REAL,
            temperature REAL,
            FOREIGN KEY(device_id) REFERENCES devices(device_id)
        )
    ''')
    
    # Optimization Results table
    c.execute('''
        CREATE TABLE IF NOT EXISTS optimization_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            energy_budget REAL,
            total_energy_used REAL,
            total_cost REAL,
            devices_selected TEXT,
            optimization_score REAL
        )
    ''')
    
    # Insert Sample Devices if table is empty
    c.execute('SELECT COUNT(*) FROM devices')
    if c.fetchone()[0] == 0:
        sample_devices = [
            ("D01", "Air Conditioner", "Cooling", 1500, 9, "ACTIVE", 4.5, 6.75, "Living Room"),
            ("D02", "Refrigerator", "Appliance", 300, 10, "ACTIVE", 24.0, 7.20, "Kitchen"),
            ("D03", "Water Heater", "Heating", 2000, 7, "INACTIVE", 1.0, 2.00, "Bathroom"),
            ("D04", "Washing Machine", "Appliance", 500, 6, "INACTIVE", 0.0, 0.00, "Laundry"),
            ("D05", "Television", "Entertainment", 120, 5, "ACTIVE", 3.0, 0.36, "Living Room"),
            ("D06", "Computer", "Electronics", 250, 8, "ACTIVE", 8.0, 2.00, "Study"),
            ("D07", "Lighting", "Lighting", 100, 4, "ACTIVE", 6.0, 0.60, "All Rooms"),
            ("D08", "Fan", "Cooling", 75, 5, "ACTIVE", 10.0, 0.75, "Bedroom")
        ]
        c.executemany('''
            INSERT INTO devices (device_id, device_name, device_type, power_watts, priority, status, operating_hours, energy_consumption, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_devices)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
