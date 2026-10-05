import React, { useEffect, useState } from 'react';
import { getHistoricalAnalytics } from '../services/api';

export default function Analytics() {
    const [data, setData] = useState(null);

    useEffect(() => {
        getHistoricalAnalytics().then(res => {
            if(!res.error) setData(res);
        });
    }, []);

    if (!data) return null;

    return (
        <div className="section-card">
            <h3 className="section-title">Historical Energy Analytics</h3>
            <div style={{ color: 'var(--text-secondary)', marginBottom: '20px', fontStyle: 'italic' }}>
                Based on historical IoT dataset (Smart_Energy_Dataset.xlsx via Pandas)
            </div>
            
            <div className="grid-cols-2">
                <div>
                    <div className="data-row"><span className="label">Total Historical Records:</span><span className="val">{data.total_records}</span></div>
                    <div className="data-row"><span className="label">Average Energy / Day:</span><span className="val">{data.average_energy_kwh} kWh</span></div>
                    <div className="data-row"><span className="label">Maximum Energy Logged:</span><span className="val">{data.max_energy_kwh} kWh</span></div>
                    <div className="data-row"><span className="label">Minimum Energy Logged:</span><span className="val">{data.min_energy_kwh} kWh</span></div>
                </div>
                <div>
                    <div className="data-row"><span className="label">Most Energy Consuming Device:</span><span className="val" style={{ color: 'var(--critical)' }}>{data.most_consuming_device}</span></div>
                    <div className="data-row"><span className="label">Total Historical Estimated Cost:</span><span className="val">${data.total_estimated_cost}</span></div>
                </div>
            </div>
        </div>
    );
}
