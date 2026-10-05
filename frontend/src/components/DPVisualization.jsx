import React from 'react';

export default function DPVisualization() {
    return (
        <div className="dp-viz">
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '10px' }}>0/1 Knapsack DP Workflow</h4>
            <div style={{ lineHeight: '1.8' }}>
                Energy Budget (Capacity W)<br/>
                ↓<br/>
                Device Selection (Item, Weight, Value)<br/>
                ↓<br/>
                Build DP Table: dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])<br/>
                ↓<br/>
                Maximum Priority Reached<br/>
                ↓<br/>
                Backtracking for Exact Devices<br/>
                ↓<br/>
                Optimal Device Set Output
            </div>
            <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'center', gap: '40px', color: 'var(--text-secondary)' }}>
                <div><strong>Time Complexity:</strong> O(n × W)</div>
                <div><strong>Space Complexity:</strong> O(n × W)</div>
            </div>
        </div>
    );
}
