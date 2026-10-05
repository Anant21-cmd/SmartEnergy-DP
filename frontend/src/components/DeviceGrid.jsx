import React from 'react';

export default function DeviceGrid({ devices }) {
    return (
        <div className="section-card">
            <h3 className="section-title">Device Dashboard</h3>
            <div className="data-grid">
                {devices.map(d => (
                    <div className="data-item" key={d.device_id}>
                        <div className="data-item-header">
                            <span className="data-name">{d.device_name}</span>
                            <span className={`status-badge ${d.status.toLowerCase()}`}>
                                {d.status}
                            </span>
                        </div>
                        <div className="data-row"><span className="label">Power:</span><span className="val">{d.power_watts} W</span></div>
                        <div className="data-row"><span className="label">Priority:</span><span className="val">{d.priority}</span></div>
                        <div className="data-row"><span className="label">Energy:</span><span className="val">{d.energy_consumption} kWh</span></div>
                        <div className="data-row"><span className="label">Type:</span><span className="val">{d.device_type}</span></div>
                    </div>
                ))}
            </div>
        </div>
    );
}
