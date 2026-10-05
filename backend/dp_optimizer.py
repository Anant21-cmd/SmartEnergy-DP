import json
from database import get_db_connection

def optimize_energy(energy_budget):
    conn = get_db_connection()
    devices = conn.execute('SELECT device_id, device_name, power_watts, priority FROM devices').fetchall()
    
    n = len(devices)
    W = int(energy_budget)
    
    # We will use power_watts as energy requirement for this context.
    # dp[i][w] = max value
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    keep = [[False for _ in range(W + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        dev = devices[i-1]
        weight = int(dev['power_watts'])
        val = dev['priority']
        
        for w in range(1, W + 1):
            if weight <= w:
                if val + dp[i-1][w-weight] > dp[i-1][w]:
                    dp[i][w] = val + dp[i-1][w-weight]
                    keep[i][w] = True
                else:
                    dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = dp[i-1][w]
                
    # Backtracking
    selected_devices = []
    total_energy_used = 0
    total_priority = 0
    w = W
    
    for i in range(n, 0, -1):
        if keep[i][w]:
            dev = devices[i-1]
            selected_devices.append(dev['device_name'])
            total_energy_used += dev['power_watts']
            total_priority += dev['priority']
            w -= int(dev['power_watts'])
            
    # Calculate score/cost
    estimated_cost = round((total_energy_used / 1000) * 0.15, 2)
    max_possible_priority = sum([d['priority'] for d in devices])
    optimization_score = round((total_priority / max_possible_priority) * 100, 2) if max_possible_priority else 0
    
    result = {
        "energy_budget": energy_budget,
        "total_energy_used": total_energy_used,
        "remaining_energy": energy_budget - total_energy_used,
        "selected_devices": selected_devices,
        "total_priority": total_priority,
        "estimated_cost": estimated_cost,
        "optimization_score": optimization_score
    }
    
    c = conn.cursor()
    c.execute('''
        INSERT INTO optimization_results (energy_budget, total_energy_used, total_cost, devices_selected, optimization_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (energy_budget, total_energy_used, estimated_cost, json.dumps(selected_devices), optimization_score))
    conn.commit()
    conn.close()
    
    return result
