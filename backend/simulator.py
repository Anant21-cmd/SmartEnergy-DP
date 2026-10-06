import random
import time
from datetime import datetime
from database import get_db_connection

def generate_sensor_data():
    conn = get_db_connection()
    devices = conn.execute('SELECT device_id, power_watts, status FROM devices').fetchall()
    
    readings = []
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for dev in devices:
        base_power = dev['power_watts'] if dev['status'] == 'ACTIVE' else 0
        
        voltage = round(random.uniform(225.0, 235.0), 1)
        if base_power > 0:
            power = round(base_power * random.uniform(0.95, 1.05), 2)
            current = round(power / voltage, 2)
            temp = round(random.uniform(25.0, 40.0), 1)
            # Just a mock small energy value for this instant reading
            energy_kwh = round((power * 1.5) / 1000, 3) 
        else:
            power = 0.0
            current = 0.0
            temp = round(random.uniform(20.0, 25.0), 1)
            energy_kwh = 0.0
            
        reading = {
            "device_id": dev['device_id'],
            "timestamp": timestamp,
            "voltage": voltage,
            "current": current,
            "power": power,
            "energy_kwh": energy_kwh,
            "temperature": temp
        }
        readings.append(reading)
        
        c.execute('''
            INSERT INTO sensor_readings (device_id, timestamp, voltage, current, power, energy_kwh, temperature)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (reading['device_id'], reading['timestamp'], reading['voltage'], reading['current'], reading['power'], reading['energy_kwh'], reading['temperature']))
        
        c.execute('''
            INSERT INTO events (device_id, event_type, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (reading['device_id'], 'SENSOR_UPDATE', f"New IoT sensor reading received ({reading['power']} W)", reading['timestamp']))
        
    conn.commit()
    conn.close()
    return readings

if __name__ == '__main__':
    print(generate_sensor_data())
