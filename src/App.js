import React, { useState } from 'react';

function App() {
  const [activeModule, setActiveModule] = useState('claims-hawk');
  const [riskScore, setRiskScore] = useState(0);
  const [incidentData, setIncidentData] = useState({
    location: '',
    dateTime: '',
    description: '',
    injuries: false,
    propertyDamage: false
  });

  const calculateRiskScore = () => {
    let score = 0;
    if (incidentData.injuries) score += 40;
    if (incidentData.propertyDamage) score += 30;
    if (incidentData.description.length > 100) score += 20;
    if (incidentData.location && incidentData.dateTime) score += 10;
    setRiskScore(score);
  };

  const modules = [
    { id: 'claims-hawk', name: 'Claims Hawk-Eye', icon: '🔍' },
    { id: 'underwriting', name: 'Underwriting AI', icon: '📊' },
    { id: 'policy-qa', name: 'Policy Q&A', icon: '❓' },
    { id: 'validator', name: 'Smart Validator', icon: '✓' },
    { id: 'agent-workflow', name: 'Agent Workflow', icon: '🔄' },
    { id: 'smart-shopper', name: 'Smart Shopper', icon: '🛒' }
  ];

  return (
    <div className="app">
      <div className="sidebar">
        <div className="logo">
          <h1>PolicyMe <span className="cortex">Cortex</span></h1>
          <div className="status">
            <span className="status-dot"></span>
            LangGraph Connected
          </div>
        </div>
        <nav className="nav-menu">
          {modules.map(module => (
            <button
              key={module.id}
              className={`nav-item ${activeModule === module.id ? 'active' : ''}`}
              onClick={() => setActiveModule(module.id)}
            >
              <span className="icon">{module.icon}</span>
              {module.name}
            </button>
          ))}
        </nav>
        <div className="user-profile">
          <div className="avatar">SA</div>
          <div className="user-info">
            <div className="user-name">Saikat A.</div>
            <div className="user-role">Full Stack Engineer</div>
          </div>
        </div>
      </div>

      <div className="main-content">
        <div className="content-header">
          <h2>Claims Intelligence Dashboard</h2>
          <div className="telemetry">
            <div className="telemetry-item">
              <span className="label">Active Claims:</span>
              <span className="value">247</span>
            </div>
            <div className="telemetry-item">
              <span className="label">Fraud Detected:</span>
              <span className="value">12</span>
            </div>
            <div className="telemetry-item">
              <span className="label">Processing Time:</span>
              <span className="value">2.3s</span>
            </div>
          </div>
        </div>

        {activeModule === 'claims-hawk' && (
          <div className="module-content">
            <div className="incident-form">
              <h3>Incident Report</h3>
              <div className="form-group">
                <label>Location</label>
                <input
                  type="text"
                  value={incidentData.location}
                  onChange={(e) => setIncidentData({...incidentData, location: e.target.value})}
                  placeholder="Enter incident location"
                />
              </div>
              <div className="form-group">
                <label>Date & Time</label>
                <input
                  type="datetime-local"
                  value={incidentData.dateTime}
                  onChange={(e) => setIncidentData({...incidentData, dateTime: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={incidentData.description}
                  onChange={(e) => setIncidentData({...incidentData, description: e.target.value})}
                  placeholder="Describe the incident in detail"
                  rows="4"
                />
              </div>
              <div className="checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={incidentData.injuries}
                    onChange={(e) => setIncidentData({...incidentData, injuries: e.target.checked})}
                  />
                  Injuries Reported
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={incidentData.propertyDamage}
                    onChange={(e) => setIncidentData({...incidentData, propertyDamage: e.target.checked})}
                  />
                  Property Damage
                </label>
              </div>
              <button className="analyze-btn" onClick={calculateRiskScore}>
                Analyze Risk
              </button>
            </div>

            <div className="risk-analysis">
              <h3>Risk Assessment</h3>
              <div className="risk-score">
                <div className="score-circle" style={{
                  background: `conic-gradient(#00d4ff ${riskScore}%, #2a2a3e ${riskScore}%)`
                }}>
                  <div className="score-inner">
                    <span className="score-value">{riskScore}</span>
                    <span className="score-label">Risk Score</span>
                  </div>
                </div>
              </div>
              <div className="risk-factors">
                <div className="factor">
                  <span className="factor-name">Injury Severity</span>
                  <div className="factor-bar">
                    <div className="factor-fill" style={{width: incidentData.injuries ? '70%' : '0%'}}></div>
                  </div>
                </div>
                <div className="factor">
                  <span className="factor-name">Property Impact</span>
                  <div className="factor-bar">
                    <div className="factor-fill" style={{width: incidentData.propertyDamage ? '60%' : '0%'}}></div>
                  </div>
                </div>
                <div className="factor">
                  <span className="factor-name">Documentation</span>
                  <div className="factor-bar">
                    <div className="factor-fill" style={{width: incidentData.description.length > 50 ? '80%' : '20%'}}></div>
                  </div>
                </div>
              </div>
              <div className="upload-evidence">
                <button className="upload-btn">📎 Upload Evidence</button>
                <p className="upload-hint">Drag & drop files or click to browse</p>
              </div>
            </div>
          </div>
        )}

        {activeModule !== 'claims-hawk' && (
          <div className="module-content">
            <div className="coming-soon">
              <h3>{modules.find(m => m.id === activeModule)?.name}</h3>
              <p>This module is coming soon. Stay tuned for updates!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
