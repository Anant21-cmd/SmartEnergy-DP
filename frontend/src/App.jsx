import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Statistics from './components/Statistics';
import DeviceGrid from './components/DeviceGrid';
import SensorMonitor from './components/SensorMonitor';
import OptimizationPanel from './components/OptimizationPanel';
import Analytics from './components/Analytics';
import { getDevices, getSensorReadings, getEnergySummary, simulateSensorData } from './services/api';

function App() {
    const [devices, setDevices] = useState([]);
    const [readings, setReadings] = useState([]);
    const [summary, setSummary] = useState(null);

    const loadData = async () => {
        try {
            const [devData, readData, sumData] = await Promise.all([
                getDevices(),
                getSensorReadings(),
                getEnergySummary()
            ]);
            setDevices(devData);
            setReadings(readData);
            setSummary(sumData);
        } catch (e) {
            console.error("Failed fetching data", e);
        }
    };

    useEffect(() => {
        loadData();
        const interval = setInterval(loadData, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleSimulate = async () => {
        await simulateSensorData();
        loadData();
    };

    return (
        <div className="dashboard-container">
            <Header />
            
            <Statistics summary={summary} />

            <div className="grid-cols-2">
                <DeviceGrid devices={devices} />
                <SensorMonitor readings={readings} onSimulate={handleSimulate} />
            </div>

            <OptimizationPanel currentEnergy={summary?.total_power || 0} />
            
            <Analytics />
        </div>
    );
}

export default App;
