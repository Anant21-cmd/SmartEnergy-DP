import React from 'react';

export default function NetworkStatus({ lastUpdate }) {
    return (
        <div className="section-card">
            <h3 className="section-title">IoT Network Status</h3>
            <div className="network-grid">
                <div className="network-item">
                    <span className="label">ESP32 Devices</span>
                    <span className="status-badge on">● 8 ONLINE</span>
                </div>
                <div className="network-item">
                    <span className="label">Sensors</span>
                    <span className="status-badge on">● 8 ONLINE</span>
                </div>
                <div className="network-item">
                    <span className="label">MQTT Broker</span>
                    <span className="status-badge on">● CONNECTED</span>
                </div>
                <div className="network-item">
                    <span className="label">Node-RED</span>
                    <span className="status-badge on">● CONNECTED</span>
                </div>
                <div className="network-item">
                    <span className="label">Backend</span>
                    <span className="status-badge on">● ONLINE</span>
                </div>
                <div className="network-item">
                    <span className="label">Database</span>
                    <span className="status-badge on">● ONLINE</span>
                </div>
            </div>
            <div style={{ marginTop: '15px', color: 'var(--text-secondary)', fontSize: '0.9rem', textAlign: 'right' }}>
                Last Sensor Update: <span style={{ color: 'var(--text-primary)' }}>{lastUpdate || 'Waiting...'}</span>
            </div>
        </div>
    );
}
