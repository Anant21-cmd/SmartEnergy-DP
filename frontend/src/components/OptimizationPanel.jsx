import React, { useState } from 'react';
import { optimizeEnergy } from '../services/api';
import DPVisualization from './DPVisualization';

export default function OptimizationPanel({ onOptimized, currentEnergy }) {
    const [budget, setBudget] = useState(5000);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleOptimize = async () => {
        setLoading(true);
        try {
            const data = await optimizeEnergy(budget);
            if (data.success) {
                setResult(data);
                if (onOptimized) onOptimized(data);
            }
        } catch (error) {
            console.error(error);
        }
        setLoading(false);
    };

    return (
        <div className="section-card">
            <h3 className="section-title">Energy Optimization (Dynamic Programming)</h3>
            
            <div className="dp-panel">
                <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                    <span style={{ fontSize: '1.2rem' }}>Available Energy Budget (Wh):</span>
                    <input 
                        type="number" 
                        className="input-number" 
                        value={budget} 
                        onChange={(e) => setBudget(Number(e.target.value))}
                    />
                    <button className="btn-primary" onClick={handleOptimize} disabled={loading}>
                        {loading ? 'CALCULATING...' : 'OPTIMIZE ENERGY'}
                    </button>
                </div>

                <DPVisualization />

                {result && (
                    <div className="dp-results">
                        <h4 style={{ color: 'var(--accent-primary)', marginBottom: '16px' }}>OPTIMAL DEVICE SCHEDULE</h4>
                        
                        <div className="grid-cols-2" style={{ marginBottom: '24px' }}>
                            <div>
                                <div className="data-row"><span className="label">Energy Budget:</span><span className="val">{result.energy_budget} Wh</span></div>
                                <div className="data-row"><span className="label">Total Energy Used:</span><span className="val">{result.total_energy_used} Wh</span></div>
                                <div className="data-row"><span className="label">Remaining Energy:</span><span className="val">{result.remaining_energy} Wh</span></div>
                            </div>
                            <div>
                                <div className="data-row"><span className="label">Total Priority Score:</span><span className="val">{result.total_priority}</span></div>
                                <div className="data-row"><span className="label">Estimated Cost:</span><span className="val">${result.estimated_cost}</span></div>
                                <div className="data-row"><span className="label">Optimization Score:</span><span className="val" style={{ color: 'var(--success)'}}>{result.optimization_score}%</span></div>
                            </div>
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <div className="data-row" style={{ marginBottom: '8px' }}>
                                <span className="label">Selected Devices:</span>
                            </div>
                            <ul className="result-list">
                                {result.selected_devices.map(d => <li key={d}>{d}</li>)}
                            </ul>
                        </div>

                        <div className="grid-cols-2" style={{ borderTop: '1px solid var(--border-color)', paddingTop: '20px' }}>
                            <div style={{ textAlign: 'center' }}>
                                <div className="label" style={{ marginBottom: '8px' }}>BEFORE OPTIMIZATION</div>
                                <div className="stat-value">{currentEnergy} Wh</div>
                            </div>
                            <div style={{ textAlign: 'center' }}>
                                <div className="label" style={{ marginBottom: '8px' }}>AFTER OPTIMIZATION</div>
                                <div className="stat-value" style={{ color: 'var(--success)'}}>{result.total_energy_used} Wh</div>
                                <div className="label" style={{ marginTop: '8px', color: 'var(--success)' }}>
                                    SAVED: {currentEnergy > result.total_energy_used ? (currentEnergy - result.total_energy_used) : 0} Wh
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
