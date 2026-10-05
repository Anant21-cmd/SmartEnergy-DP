import React from 'react';

export default function SensorMonitor({ readings, onSimulate }) {
    return (
        <div className="section-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h3 className="section-title" style={{ margin: 0 }}>Live Sensor Data</h3>
                <button className="btn-secondary" onClick={onSimulate}>Simulate Next Reading</button>
            </div>
            
            <div className="data-grid">
                {readings.map((r, i) => (
                    <div className="data-item" key={i}>
                        <div className="data-item-header">
                            <span className="data-name">{r.device_name} Sensor</span>
                        </div>
                        <div className="data-row"><span className="label">Voltage:</span><span className="val">{r.voltage} V</span></div>
                        <div className="data-row"><span className="label">Current:</span><span className="val">{r.current} A</span></div>
                        <div className="data-row"><span className="label">Power:</span><span className="val">{r.power} W</span></div>
                        <div className="data-row"><span className="label">Energy:</span><span className="val">{r.energy_kwh} kWh</span></div>
                        <div className="data-row"><span className="label">Temp:</span><span className="val">{r.temperature} °C</span></div>
                        <div className="data-row" style={{ fontSize: '0.8rem', marginTop: '8px' }}>
                            <span className="label">Time:</span>
                            <span className="val" style={{ color: 'var(--accent-secondary)' }}>{r.timestamp}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
