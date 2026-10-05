const API_BASE_URL = 'http://127.0.0.1:5000/api';

export const getDevices = async () => {
    const res = await fetch(`${API_BASE_URL}/devices`);
    return res.json();
};

export const getDevice = async (deviceId) => {
    const res = await fetch(`${API_BASE_URL}/device/${deviceId}`);
    return res.json();
};

export const getSensorReadings = async () => {
    const res = await fetch(`${API_BASE_URL}/sensor-readings`);
    return res.json();
};

export const getEnergySummary = async () => {
    const res = await fetch(`${API_BASE_URL}/energy-summary`);
    return res.json();
};

export const simulateSensorData = async () => {
    const res = await fetch(`${API_BASE_URL}/simulate`, { method: 'POST' });
    return res.json();
};

export const optimizeEnergy = async (budget) => {
    const res = await fetch(`${API_BASE_URL}/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ energy_budget: budget })
    });
    return res.json();
};

export const getOptimizationHistory = async () => {
    const res = await fetch(`${API_BASE_URL}/optimization-history`);
    return res.json();
};

export const getHistoricalAnalytics = async () => {
    const res = await fetch(`${API_BASE_URL}/historical-analytics`);
    return res.json();
};
