import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { ArrowLeftIcon, AlertTriangleIcon, CheckCircleIcon } from '../components/Icons';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function AnalysisDetailPage() {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);

  useDocumentTitle('Analysis Detail');
  const { addToast } = useToast();

  useEffect(() => {
    fetchAnalysis();
  }, [id]);

  const fetchAnalysis = async () => {
    try {
      const res = await api.get(`/api/analysis/${id}`);
      setAnalysis(res.data);
    } catch (err) {
      addToast('Analysis not found', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page-loading"><div className="spinner" /></div>;
  if (!analysis) return <div className="empty-state"><p>Analysis not found.</p></div>;

  return (
    <div className="page">
      <div className="page-header">
        <Link to="/history" className="btn btn-outline btn-sm"><ArrowLeftIcon size={16} /> Back to History</Link>
      </div>

      <div className="detail-card">
        <div className="detail-banner-row">
          <div className={`result-banner result-${analysis.prediction}`}>
            {analysis.prediction === 'spam' ? <AlertTriangleIcon size={32} /> : <CheckCircleIcon size={32} />}
            <div>
              <h2>{analysis.prediction === 'spam' ? 'SPAM DETECTED' : 'LEGITIMATE EMAIL'}</h2>
              <p>{analysis.confidence}% confidence</p>
            </div>
          </div>
          <div className="confidence-animation">
            <div className="confidence-ring confidence-ring-sm" style={{ '--conf': `${analysis.confidence}%`, '--ring-color': analysis.prediction === 'spam' ? 'var(--color-error)' : 'var(--color-success)' }}>
              <div className="confidence-ring-inner">
                <span className="confidence-ring-value">{analysis.confidence}%</span>
                <span className="confidence-ring-label">Confidence</span>
              </div>
            </div>
          </div>
        </div>

        <div className="detail-grid">
          <div className="detail-section">
            <h3>Email Details</h3>
            <div className="detail-row"><span className="detail-label">From:</span><span>{analysis.sender || 'Unknown'}</span></div>
            <div className="detail-row"><span className="detail-label">Subject:</span><span>{analysis.subject || 'No subject'}</span></div>
            <div className="detail-row"><span className="detail-label">Analyzed:</span><span>{new Date(analysis.created_at).toLocaleString()}</span></div>
            <div className="detail-row"><span className="detail-label">Model:</span><span>{analysis.algorithm} ({analysis.model_version})</span></div>
            <div className="detail-row"><span className="detail-label">Risk:</span><span className={`risk-badge risk-${analysis.risk_level}`}>{analysis.risk_level.toUpperCase()}</span></div>
          </div>

          <div className="detail-section">
            <h3>Email Body</h3>
            <div className="email-body-preview">{analysis.body}</div>
          </div>
        </div>

        {analysis.indicators && analysis.indicators.length > 0 && (
          <div className="detail-section">
            <h3>Detection Indicators</h3>
            <p className="disclaimer">These are indicators identified by the ML model, not absolute proof.</p>
            <div className="indicators-list">
              {analysis.indicators.map((ind, i) => (
                <div key={i} className={`indicator indicator-${ind.severity}`}>
                  <span className={`severity-dot severity-${ind.severity}`} />
                  <span className="indicator-desc">{ind.description}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
