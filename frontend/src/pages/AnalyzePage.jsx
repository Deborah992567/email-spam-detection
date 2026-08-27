import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { MailIcon, ShieldIcon, AlertTriangleIcon, CheckCircleIcon } from '../components/Icons';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function AnalyzePage() {
  const [sender, setSender] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const { addToast } = useToast();
  const navigate = useNavigate();

  useDocumentTitle('Analyze Email');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!body.trim()) {
      addToast('Please enter email body', 'error');
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const res = await api.post('/api/analysis/', { sender, subject, body });
      setResult(res.data);
      addToast('Analysis complete', 'success');
    } catch (err) {
      addToast(err.response?.data?.detail || 'Analysis failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setSender('');
    setSubject('');
    setBody('');
    setResult(null);
  };

  const fillSample = () => {
    setSender('prize-claims@winbig.example.com');
    setSubject('CONGRATULATIONS! You have WON $10,000 - Claim now!!!');
    setBody(
      'Dear winner,\n\nCONGRATULATIONS!!! You have been selected to receive a cash prize of $10,000 USD!!! ' +
      'To claim your reward, simply click the link below and enter your bank details within 24 hours.\n\n' +
      'This offer is 100% FREE and expires immediately. Do not miss this limited time opportunity!\n\n' +
      'Click here to claim your prize now!\n\nBest regards,\nClaims Department'
    );
    setResult(null);
  };

  if (result) {
    return (
      <div className="page">
        <div className="page-header">
          <h1>Analysis Result</h1>
        </div>
        <div className="result-card">
          <div className={`result-banner result-${result.prediction}`}>
            {result.prediction === 'spam' ? <AlertTriangleIcon size={32} /> : <CheckCircleIcon size={32} />}
            <div>
              <h2>{result.prediction === 'spam' ? 'SPAM DETECTED' : 'LEGITIMATE EMAIL'}</h2>
              <p>Classification: <strong>{result.prediction.toUpperCase()}</strong></p>
            </div>
          </div>

          <div className="result-details">
            <div className="result-metrics">
              <div className="metric">
                <span className="metric-label">Confidence</span>
                <span className="metric-value">{result.confidence}%</span>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${result.confidence}%`, background: result.prediction === 'spam' ? 'var(--color-error)' : 'var(--color-success)' }} />
                </div>
              </div>
              <div className="metric">
                <span className="metric-label">Risk Level</span>
                <span className={`risk-badge risk-${result.risk_level}`}>{result.risk_level.toUpperCase()}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Model</span>
                <span className="metric-value-sm">{result.algorithm} ({result.model_version})</span>
              </div>
              <div className="metric">
                <span className="metric-label">Analyzed At</span>
                <span className="metric-value-sm">{new Date(result.created_at).toLocaleString()}</span>
              </div>
            </div>

            {result.indicators && result.indicators.length > 0 && (
              <div className="indicators-section">
                <h3>Indicators</h3>
                <p className="disclaimer">These are indicators, not absolute proof. The ML model identifies patterns that may suggest spam.</p>
                <div className="indicators-list">
                  {result.indicators.map((ind, i) => (
                    <div key={i} className={`indicator indicator-${ind.severity}`}>
                      <span className={`severity-dot severity-${ind.severity}`} />
                      <div>
                        <span className="indicator-desc">{ind.description}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="result-actions">
            <button className="btn btn-primary" onClick={resetForm}>Analyze Another Email</button>
            <button className="btn btn-outline" onClick={() => navigate('/history')}>View History</button>
            {result.id && <button className="btn btn-outline" onClick={() => navigate(`/history/${result.id}`)}>View Full Report</button>}
          </div>

          <div className="confidence-animation">
            <div className="confidence-ring" style={{ '--conf': `${result.confidence}%`, '--ring-color': result.prediction === 'spam' ? 'var(--color-error)' : 'var(--color-success)' }}>
              <div className="confidence-ring-inner">
                <span className="confidence-ring-value">{result.confidence}%</span>
                <span className="confidence-ring-label">Confidence</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Analyze Email</h1>
        <div className="page-header-actions">
          <button type="button" className="btn btn-outline" onClick={fillSample}>Try Sample Email</button>
        </div>
      </div>
      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Sender Email</label>
            <input type="email" value={sender} onChange={e => setSender(e.target.value)} placeholder="sender@example.com" />
          </div>
          <div className="form-group">
            <label>Subject</label>
            <input type="text" value={subject} onChange={e => setSubject(e.target.value)} placeholder="Email subject line" />
          </div>
          <div className="form-group">
            <label>Email Body <span className="required">*</span></label>
            <textarea value={body} onChange={e => setBody(e.target.value)} placeholder="Paste the email content here..." rows={12} required />
            <div className="form-hint">{body.length} characters · Minimum recommended: 20</div>
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? <><div className="spinner-sm" /> Analyzing...</> : <><MailIcon size={18} /> Analyze Email</>}
          </button>
        </form>
      </div>
    </div>
  );
}
