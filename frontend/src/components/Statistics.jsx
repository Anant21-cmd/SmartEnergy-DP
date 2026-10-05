import React from 'react';

export default function Statistics({ summary }) {
    if (!summary) return <div>Loading statistics...</div>;
    return (
        <div className="section-card">
            <h3 className="section-title">Energy Summary</h3>
            <div className="stats-grid">
                <div className="stat-box">
                    <div className="stat-label">Total Devices</div>
                    <div className="stat-value">{summary.total_devices}</div>
                </div>
                <div className="stat-box">
                    <div className="stat-label">Active Devices</div>
                    <div className="stat-value">{summary.active_devices}</div>
                </div>
                <div className="stat-box">
                    <div className="stat-label">Current Power</div>
                    <div className="stat-value highlight">{summary.total_power} W</div>
                </div>
                <div className="stat-box">
                    <div className="stat-label">Today's Energy</div>
                    <div className="stat-value">{summary.today_energy} kWh</div>
                </div>
                <div className="stat-box">
                    <div className="stat-label">Estimated Cost</div>
                    <div className="stat-value">${summary.estimated_cost}</div>
                </div>
                <div className="stat-box">
                    <div className="stat-label">Peak Power</div>
                    <div className="stat-value">{summary.peak_power} W</div>
                </div>
            </div>
        </div>
    );
}
