import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { BrainIcon, PlayIcon, CheckCircleIcon, DatabaseIcon } from '../components/Icons';

export default function ModelPerformance() {
  const [versions, setVersions] = useState([]);
  const [currentModel, setCurrentModel] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [training, setTraining] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [trainResult, setTrainResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useEffect(() => { fetchData(); }, []);

  const fetchData = async () => {
    try {
      const [verRes, curRes, dsRes] = await Promise.all([
        api.get('/api/model/versions'),
        api.get('/api/model/current'),
        api.get('/api/model/dataset-status'),
      ]);
      setVersions(verRes.data);
      setCurrentModel(curRes.data);
      setDataset(dsRes.data);
    } catch (err) {
      addToast('Failed to load model data', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSeedAndTrain = async () => {
    if (!confirm('No training data found. Seed the app with SAMPLE data (for development) and train the model automatically? This is NOT production data.')) return;
    setSeeding(true);
    setTrainResult(null);
    try {
      const res = await api.post('/api/model/seed-and-train');
      setTrainResult({
        ...res.data,
        results: { [res.data.best_model]: res.data.metrics ? { ...res.data.metrics } : {} },
        train_size: Math.round(res.data.total_samples * 0.8),
        test_size: res.data.total_samples - Math.round(res.data.total_samples * 0.8),
      });
      addToast('Sample data seeded and model trained!', 'success');
      fetchData();
    } catch (err) {
      addToast(err.response?.data?.detail || 'Seeding/training failed', 'error');
    } finally {
      setSeeding(false);
    }
  };

  const handleTrain = async () => {
    if (!confirm('This will train a new model using all training samples. Continue?')) return;
    setTraining(true);
    setTrainResult(null);
    try {
      const res = await api.post('/api/model/train');
      setTrainResult(res.data);
      addToast('Model trained successfully!', 'success');
      fetchData();
    } catch (err) {
      addToast(err.response?.data?.detail || 'Training failed', 'error');
    } finally {
      setTraining(false);
    }
  };

  if (loading) return <div className="page-loading"><div className="spinner" /></div>;

  const canTrain = dataset && dataset.enough_to_train;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Model Performance</h1>
        <div className="page-header-actions">
          {!canTrain && (
            <button className="btn btn-outline" onClick={handleSeedAndTrain} disabled={seeding}>
              {seeding ? <><div className="spinner-sm" /> Seeding &amp; Training...</> : <><DatabaseIcon size={18} /> Seed Sample Data &amp; Train</>}
            </button>
          )}
          <button className="btn btn-primary" onClick={handleTrain} disabled={training || !canTrain}>
            {training ? <><div className="spinner-sm" /> Training...</> : <><PlayIcon size={18} /> Train/Retrain Model</>}
          </button>
        </div>
      </div>

      {dataset && (
        <div className="card dataset-card">
          <h3><DatabaseIcon size={18} /> Training Dataset</h3>
          <div className="model-info-grid">
            <div className="model-info-item"><span className="label">Total Samples:</span><span className="value">{dataset.total}</span></div>
            <div className="model-info-item"><span className="label">Spam:</span><span className="value">{dataset.spam}</span></div>
            <div className="model-info-item"><span className="label">Ham:</span><span className="value">{dataset.ham}</span></div>
            <div className="model-info-item"><span className="label">Source:</span><span className="value">{dataset.source === 'sample' ? 'Sample (dev)' : 'Dataset'}</span></div>
            <div className="model-info-item"><span className="label">Ready to Train:</span><span className={`badge ${canTrain ? 'badge-success' : 'badge-warning'}`}>{canTrain ? 'Yes' : 'No'}</span></div>
          </div>
          {!canTrain && (
            <p className="dataset-note">
              No sufficient training data detected. If you don't have a real dataset yet, use
              <strong> Seed Sample Data &amp; Train</strong> to load clearly-labeled development samples and train a
              working model automatically. For production use, upload a real dataset via the Dataset page instead.
            </p>
          )}
        </div>
      )}

      {currentModel && currentModel.status !== 'no_model' && (
        <div className="card">
          <h3>Current Model</h3>
          <div className="model-info-grid">
            <div className="model-info-item"><span className="label">Version:</span><span className="value">{currentModel.version}</span></div>
            <div className="model-info-item"><span className="label">Algorithm:</span><span className="value">{currentModel.algorithm}</span></div>
            <div className="model-info-item"><span className="label">Accuracy:</span><span className="value">{(currentModel.accuracy * 100).toFixed(1)}%</span></div>
            <div className="model-info-item"><span className="label">F1 Score:</span><span className="value">{(currentModel.f1_score * 100).toFixed(1)}%</span></div>
            <div className="model-info-item"><span className="label">Trained:</span><span className="value">{new Date(currentModel.trained_at).toLocaleString()}</span></div>
          </div>
        </div>
      )}

      {trainResult && (
        <div className="card">
          <h3><CheckCircleIcon size={20} /> Training Results</h3>
          <p>Best model: <strong>{trainResult.best_model}</strong> ({trainResult.train_size} train / {trainResult.test_size} test samples)</p>
          <div className="table-responsive">
            <table className="table">
              <thead><tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1 Score</th></tr></thead>
              <tbody>
                {Object.entries(trainResult.results).map(([name, m]) => (
                  <tr key={name} className={name === trainResult.best_model ? 'row-highlight' : ''}>
                    <td>{name} {name === trainResult.best_model && <span className="badge badge-success">Best</span>}</td>
                    <td>{(m.accuracy * 100).toFixed(1)}%</td>
                    <td>{(m.precision * 100).toFixed(1)}%</td>
                    <td>{(m.recall * 100).toFixed(1)}%</td>
                    <td>{(m.f1_score * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="card">
        <h3>Model Version History</h3>
        {versions.length > 0 ? (
          <div className="table-responsive">
            <table className="table">
              <thead><tr><th>Version</th><th>Algorithm</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>Trained</th></tr></thead>
              <tbody>
                {versions.map(v => (
                  <tr key={v.id}>
                    <td><span className="badge badge-info">{v.version}</span></td>
                    <td>{v.algorithm}</td>
                    <td>{(v.accuracy * 100).toFixed(1)}%</td>
                    <td>{(v.precision * 100).toFixed(1)}%</td>
                    <td>{(v.recall * 100).toFixed(1)}%</td>
                    <td>{(v.f1_score * 100).toFixed(1)}%</td>
                    <td>{new Date(v.trained_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <BrainIcon size={48} />
            <p>No model versions yet. Train a model to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
}
