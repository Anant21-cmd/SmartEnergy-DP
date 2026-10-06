import React, { useEffect, useState } from 'react';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default function RecentEvents() {
    const [events, setEvents] = useState([]);

    const loadEvents = async () => {
        try {
            const res = await fetch(`${API_BASE_URL}/recent-events`);
            const data = await res.json();
            setEvents(data);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        loadEvents();
        const interval = setInterval(loadEvents, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="section-card">
            <h3 className="section-title">Recent Events</h3>
            <div className="events-list">
                {events.length === 0 ? <p style={{color: 'var(--text-secondary)'}}>No recent events.</p> : null}
                {events.map((e, idx) => {
                    const time = new Date(e.timestamp).toLocaleTimeString();
                    return (
                        <div className="event-item" key={idx}>
                            <div className="event-time">{time}</div>
                            <div className="event-msg">
                                <strong>{e.device_id}</strong>: {e.message}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
