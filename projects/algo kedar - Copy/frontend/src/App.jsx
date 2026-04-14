import React, { useState } from 'react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave" || e.type === "drop") {
      setDragActive(false);
    }
  };

  const processFile = (selectedFile) => {
    if (selectedFile && selectedFile.name.endsWith('.teal')) {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    } else {
      setError("Please upload a valid .teal smart contract file.");
      setFile(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMsg = 'Analysis failed. Please try again.';
        try {
          const errData = await response.json();
          errorMsg = errData.detail || errorMsg;
        } catch (e) {
          console.debug("Non-JSON error response", e);
        }
        throw new Error(errorMsg);
      }

      const data = await response.json();
      // Ensure smooth visual transition delay
      setTimeout(() => {
        setResult(data);
        setLoading(false);
      }, 600);
      
    } catch (err) {
      setTimeout(() => {
        setError(err.message);
        setLoading(false);
      }, 600);
    }
  };

  const formatFeatureName = (name) => {
    return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  const getStatusIcon = (label) => {
    if (label === 'SAFE') return <span style={{ marginRight: '16px', fontSize: '32px' }}>✅</span>;
    if (label === 'SUSPICIOUS') return <span style={{ marginRight: '16px', fontSize: '32px' }}>⚠️</span>;
    return <span style={{ marginRight: '16px', fontSize: '32px' }}>❌</span>;
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>AlgoShield AI</h1>
        <p>Intelligent Security Analysis for Algorand TEAL Smart Contracts</p>
      </header>

      <main>
        <div className="glass-card">
          <div 
            className={`file-upload-area ${dragActive ? 'drag-active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-upload').click()}
          >
            <input 
              type="file" 
              id="file-upload" 
              accept=".teal" 
              style={{ display: 'none' }} 
              onChange={handleChange}
            />
            <div className="upload-icon" style={{ fontSize: '48px' }}>📁</div>
            
            {file ? (
              <div style={{ animation: 'slideUp 0.3s ease' }}>
                <h3 style={{ color: '#60a5fa', fontSize: '1.4rem', marginBottom: '0.5rem' }}>{file.name}</h3>
                <p style={{ color: 'var(--text-muted)' }}>Click or drag a different file to replace</p>
              </div>
            ) : (
              <div>
                <h3 style={{ fontSize: '1.4rem', marginBottom: '0.5rem' }}>Upload your TEAL file</h3>
                <p style={{ color: 'var(--text-muted)' }}>Drag and drop or click to browse</p>
              </div>
            )}
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button 
            className="btn" 
            onClick={handleAnalyze} 
            disabled={!file || loading}
          >
            {loading ? <div className="loading-spinner"></div> : 'Analyze Smart Contract'}
          </button>
        </div>

        {result && (
          <div className="glass-card result-container" style={{ marginTop: '2rem' }}>
            <h2 style={{ marginBottom: '2rem', color: 'var(--text-muted)', fontSize: '1.2rem', textTransform: 'uppercase', letterSpacing: '1px' }}>
              Security Assessment Result
            </h2>
            
            <div className={`status-badge status-${result.label.toLowerCase()}`}>
              {getStatusIcon(result.label)}
              {result.label}
            </div>

            <div style={{ width: '100%', textAlign: 'left', marginTop: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div style={{ height: '1px', flex: 1, background: 'var(--glass-border)' }}></div>
                <h3 style={{ margin: '0 1rem', color: '#cbd5e1', fontSize: '1.1rem' }}>Extracted Features</h3>
                <div style={{ height: '1px', flex: 1, background: 'var(--glass-border)' }}></div>
              </div>

              <div className="features-grid">
                {Object.entries(result.features).map(([key, value]) => (
                  <div className="feature-item" key={key}>
                    <span className="feature-label">{formatFeatureName(key)}</span>
                    <span className="feature-value">
                      {typeof value === 'number' ? (Number.isInteger(value) ? value : value.toFixed(4)) : value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
