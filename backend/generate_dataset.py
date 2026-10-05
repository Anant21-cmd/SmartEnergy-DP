import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_dataset():
    # 30 days of data for 8 devices
    devices = ['D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08']
    
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    
    records = []
    
    for d in dates:
        for dev in devices:
            base_power = {
                'D01': 1500, 'D02': 300, 'D03': 2000, 
                'D04': 500, 'D05': 120, 'D06': 250, 
                'D07': 100, 'D08': 75
            }[dev]
            
            hours_run = np.random.uniform(2, 12) if dev != 'D02' else 24 # Fridge runs 24h
            daily_energy = (base_power * hours_run) / 1000
            
            records.append({
                'Date': d.strftime('%Y-%m-%d'),
                'DeviceID': dev,
                'HoursRun': round(hours_run, 2),
                'EnergyKWh': round(daily_energy, 2),
                'CostEstimate': round(daily_energy * 0.15, 2) # $0.15 per kWh
            })
            
    df = pd.DataFrame(records)
    df.to_excel('Smart_Energy_Dataset.xlsx', index=False)
    print("Dataset generated")

if __name__ == '__main__':
    create_dataset()
