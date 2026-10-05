import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "smartenergy/dp/sensors"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected successfully to MQTT Broker ({MQTT_BROKER})")
    else:
        print(f"Failed to connect, return code {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print("Connecting to MQTT Broker...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Devices to simulate
devices = [
    {"id": "D01", "name": "Air Conditioner", "base_power": 1500},
    {"id": "D02", "name": "Refrigerator", "base_power": 300},
    {"id": "D06", "name": "Computer", "base_power": 250},
    {"id": "D08", "name": "Fan", "base_power": 75}
]

try:
    print("\n--- ESP32 MQTT SIMULATOR STARTED ---")
    print(f"Publishing to topic: {MQTT_TOPIC}")
    print("Press CTRL+C to exit.\n")
    
    while True:
        # Pick a random device to send data for
        dev = random.choice(devices)
        
        voltage = round(random.uniform(225.0, 235.0), 1)
        power = round(dev['base_power'] * random.uniform(0.95, 1.05), 2)
        current = round(power / voltage, 2)
        temp = round(random.uniform(25.0, 40.0), 1)
        energy_kwh = round((power * 1.5) / 1000, 3) 
        
        payload = {
            "device_id": dev["id"],
            "voltage": voltage,
            "current": current,
            "power": power,
            "energy_kwh": energy_kwh,
            "temperature": temp
        }
        
        json_payload = json.dumps(payload)
        client.publish(MQTT_TOPIC, json_payload)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] PUBLISHED -> {json_payload}")
        
        time.sleep(5)  # Wait 5 seconds before sending next reading
        
except KeyboardInterrupt:
    print("\nDisconnecting...")
    client.loop_stop()
    client.disconnect()
    print("Exited.")
