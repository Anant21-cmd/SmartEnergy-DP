import React from 'react';

export default function Header() {
    return (
        <header className="app-header">
            <div className="header-title">
                <h1>SMARTENERGY DP</h1>
                <h2>IoT Energy Monitoring & Dynamic Optimization</h2>
            </div>
            <div className="demo-badge">
                <span style={{ fontSize: '1.2rem' }}>●</span> DEMO / SIMULATION MODE
            </div>
        </header>
    );
}
