import React, { useState } from 'react';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default function SearchPanel() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [searched, setSearched] = useState(false);

    const handleSearch = async () => {
        if (!query) return;
        try {
            const res = await fetch(`${API_BASE_URL}/search?q=${query}`);
            const data = await res.json();
            setResults(data);
            setSearched(true);
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="section-card">
            <h3 className="section-title">Smart Energy Search</h3>
            <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
                <input 
                    type="text" 
                    className="input-text" 
                    placeholder="Search by ID, Name, Location..." 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    style={{ flex: 1 }}
                />
                <button className="btn-primary" onClick={handleSearch}>SEARCH</button>
            </div>
            
            {searched && results.length === 0 && <p style={{color: 'var(--text-secondary)'}}>No devices found.</p>}
            
            {results.length > 0 && (
                <div className="data-grid">
                    {results.map(d => (
                        <div className="data-item" key={d.device_id}>
                            <div className="data-item-header">
                                <span className="data-name">{d.device_name} ({d.device_id})</span>
                                <span className={`status-badge ${d.status.toLowerCase()}`}>{d.status}</span>
                            </div>
                            <div className="data-row"><span className="label">Location:</span><span className="val">{d.location}</span></div>
                            <div className="data-row"><span className="label">Type:</span><span className="val">{d.device_type}</span></div>
                            <div className="data-row"><span className="label">Power Rating:</span><span className="val">{d.power_watts} W</span></div>
                            {d.power !== undefined && (
                                <>
                                    <div style={{borderTop: '1px solid var(--border-color)', margin: '10px 0'}}></div>
                                    <div className="data-row"><span className="label">Live Power:</span><span className="val">{d.power} W</span></div>
                                    <div className="data-row"><span className="label">Energy:</span><span className="val">{d.energy_kwh} kWh</span></div>
                                    <div className="data-row"><span className="label">Temp:</span><span className="val">{d.temperature} °C</span></div>
                                </>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
