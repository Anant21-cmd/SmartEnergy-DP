import pandas as pd
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), 'Smart_Energy_Dataset.xlsx')

def get_historical_analytics():
    if not os.path.exists(EXCEL_PATH):
        return {"error": "Dataset not found"}
        
    df = pd.read_excel(EXCEL_PATH)
    
    total_records = len(df)
    avg_energy = round(df['EnergyKWh'].mean(), 2)
    max_energy = round(df['EnergyKWh'].max(), 2)
    min_energy = round(df['EnergyKWh'].min(), 2)
    
    # Device-wise consumption
    device_grouped = df.groupby('DeviceID')['EnergyKWh'].sum().to_dict()
    most_consuming = max(device_grouped, key=device_grouped.get)
    
    # Daily energy
    daily_grouped = df.groupby('Date')['EnergyKWh'].sum().reset_index()
    daily_energy_trend = daily_grouped.to_dict('records')
    
    total_cost = round(df['CostEstimate'].sum(), 2)
    
    return {
        "total_records": total_records,
        "average_energy_kwh": avg_energy,
        "max_energy_kwh": max_energy,
        "min_energy_kwh": min_energy,
        "device_wise_consumption": device_grouped,
        "most_consuming_device": most_consuming,
        "total_estimated_cost": total_cost,
        "daily_trend": daily_energy_trend
    }
