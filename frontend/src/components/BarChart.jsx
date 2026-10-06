import React from 'react';

export default function BarChart({ devices }) {
    // Find max power to scale bars
    const maxPower = Math.max(...devices.map(d => d.power_watts || 100), 2000);
    
    return (
        <div className="section-card">
            <h3 className="section-title">Device-wise Energy Requirements</h3>
            <div className="bar-chart-container">
                {devices.map(d => {
                    const heightPercent = ((d.power_watts || 0) / maxPower) * 100;
                    return (
                        <div className="bar-wrapper" key={d.device_id}>
                            <div className="bar" style={{ height: `${heightPercent}%` }} title={`${d.power_watts} W`}></div>
                            <div className="bar-label">{d.device_name}</div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
