import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { SearchIcon, TrashIcon, UploadIcon, DatabaseIcon, PlusIcon } from '../components/Icons';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function DatasetManagement() {
  const [samples, setSamples] = useState([]);
  const [total, setTotal] = useState(0);

  useDocumentTitle('Dataset Management');
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [search, setSearch] = useState('');
  const [labelFilter, setLabelFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [newMessage, setNewMessage] = useState('');
  const [newLabel, setNewLabel] = useState('ham');
  const [uploading, setUploading] = useState(false);
  const [adding, setAdding] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const fileRef = useRef();
  const { addToast } = useToast();

  useEffect(() => { fetchSamples(); fetchStats(); }, [page, labelFilter]);

  const fetchSamples = async () => {
    setLoading(true);
    try {
      const params = { page, per_page: 10 };
      if (search) params.search = search;
      if (labelFilter) params.label = labelFilter;
      const res = await api.get('/api/dataset/', { params });
      setSamples(res.data.items);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      addToast('Failed to load samples', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await api.get('/api/dataset/stats');
      setStats(res.data);
    } catch (err) {}
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await api.post('/api/dataset/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      addToast(res.data.message, 'success');
      fetchSamples();
      fetchStats();
    } catch (err) {
      addToast(err.response?.data?.detail || 'Upload failed', 'error');
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = '';
    }
  };

  const handleAddSample = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;
    setAdding(true);
    try {
      await api.post('/api/dataset/', { message: newMessage, label: newLabel });
      addToast('Sample added', 'success');
      setNewMessage('');
      fetchSamples();
      fetchStats();
    } catch (err) {
      addToast(err.response?.data?.detail || 'Failed to add sample', 'error');
    } finally {
      setAdding(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this training sample?')) return;
    try {
      await api.delete(`/api/dataset/${id}`);
      addToast('Sample deleted', 'success');
      fetchSamples();
      fetchStats();
    } catch (err) {
      addToast('Failed to delete', 'error');
    }
  };

  const handleSeed = async () => {
    if (!confirm('Load the built-in SAMPLE dataset for development? These are clearly-labeled sample emails (not production data).')) return;
    setSeeding(true);
    try {
      const res = await api.post('/api/model/seed-sample-data');
      addToast(`Seeded ${res.data.seeded} sample emails`, 'success');
      fetchSamples();
      fetchStats();
    } catch (err) {
      addToast(err.response?.data?.detail || 'Seeding failed', 'error');
    } finally {
      setSeeding(false);
    }
  };

  const handleDownload = async (kind) => {
    try {
      const res = await api.get(`/api/dataset/${kind}`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.download = kind === 'template' ? 'dataset_template.csv' : 'training_dataset.csv';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      addToast('Download failed', 'error');
    }
  };

  const handleClearAll = async () => {
    if (!confirm('Delete ALL training samples? This cannot be undone. You may want to export first.')) return;
    try {
      await api.delete('/api/dataset/clear-all');
      addToast('All training samples cleared', 'success');
      fetchSamples();
      fetchStats();
    } catch (err) {
      addToast('Failed to clear dataset', 'error');
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Dataset Management</h1>
        <div className="page-header-actions">
          <button className="btn btn-outline" onClick={() => handleDownload('template')}>Download Template</button>
          <button className="btn btn-outline" onClick={() => handleDownload('export')}>Export Dataset</button>
          <button className="btn btn-outline" onClick={handleSeed} disabled={seeding}>
            {seeding ? <><div className="spinner-sm" /> Seeding...</> : <><DatabaseIcon size={18} /> Seed Sample Data</>}
          </button>
          {total > 0 && <button className="btn btn-danger" onClick={handleClearAll}>Clear All</button>}
        </div>
      </div>

      {stats && (
        <div className="stats-grid stats-grid-3">
          <div className="stat-card">
            <div className="stat-icon stat-icon-blue"><DatabaseIcon size={24} /></div>
            <div className="stat-info"><span className="stat-value">{stats.total}</span><span className="stat-label">Total Samples</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon stat-icon-red"><span className="stat-value-inner">{stats.spam}</span></div>
            <div className="stat-info"><span className="stat-value">{stats.spam}</span><span className="stat-label">Spam</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon stat-icon-green"><span className="stat-value-inner">{stats.ham}</span></div>
            <div className="stat-info"><span className="stat-value">{stats.ham}</span><span className="stat-label">Ham</span></div>
          </div>
        </div>
      )}

      <div className="dataset-actions-row">
        <div className="card dataset-add-card">
          <h3>Add Sample</h3>
          <form onSubmit={handleAddSample}>
            <div className="form-group">
              <label>Message</label>
              <textarea value={newMessage} onChange={e => setNewMessage(e.target.value)} placeholder="Enter email text..." rows={3} required />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Label</label>
                <select value={newLabel} onChange={e => setNewLabel(e.target.value)}>
                  <option value="ham">Ham</option>
                  <option value="spam">Spam</option>
                </select>
              </div>
              <button type="submit" className="btn btn-primary" disabled={adding}>{adding ? 'Adding...' : 'Add Sample'}</button>
            </div>
          </form>
        </div>

        <div className="card dataset-upload-card">
          <h3>Upload CSV</h3>
          <p className="text-muted">CSV must have 'label' and 'message' columns.</p>
          <input type="file" ref={fileRef} accept=".csv" onChange={handleUpload} id="csv-upload" style={{ display: 'none' }} />
          <label htmlFor="csv-upload" className="btn btn-outline upload-btn">
            <UploadIcon size={18} /> {uploading ? 'Uploading...' : 'Choose CSV File'}
          </label>
        </div>
      </div>

      <div className="card">
        <div className="table-toolbar">
          <form onSubmit={(e) => { e.preventDefault(); setPage(1); fetchSamples(); }} className="search-form">
            <SearchIcon size={18} />
            <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search samples..." />
            <button type="submit" className="btn btn-sm btn-primary">Search</button>
          </form>
          <div className="filter-group">
            <select value={labelFilter} onChange={e => { setLabelFilter(e.target.value); setPage(1); }}>
              <option value="">All Labels</option>
              <option value="spam">Spam</option>
              <option value="ham">Ham</option>
            </select>
          </div>
        </div>

        {loading ? <div className="page-loading"><div className="spinner" /></div> : samples.length > 0 ? (
          <>
            <div className="table-responsive">
              <table className="table">
                <thead><tr><th>Message</th><th>Label</th><th>Source</th><th>Date</th><th>Actions</th></tr></thead>
                <tbody>
                  {samples.map(s => (
                    <tr key={s.id}>
                      <td className="text-truncate" style={{ maxWidth: 400 }}>{s.message}</td>
                      <td><span className={`badge badge-${s.label === 'spam' ? 'danger' : 'success'}`}>{s.label.toUpperCase()}</span></td>
                      <td>{s.source === 'sample' ? <span className="badge badge-warning">Sample</span> : <span className="badge badge-info">Dataset</span>}</td>
                      <td>{new Date(s.created_at).toLocaleDateString()}</td>
                      <td><button className="btn btn-sm btn-danger" onClick={() => handleDelete(s.id)}><TrashIcon size={14} /></button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="pagination">
              <button className="btn btn-sm btn-outline" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Prev</button>
              <span>Page {page} of {pages}</span>
              <button className="btn btn-sm btn-outline" disabled={page >= pages} onClick={() => setPage(p => p + 1)}>Next</button>
            </div>
          </>
        ) : <div className="empty-state"><DatabaseIcon size={48} /><p>No training samples. Add samples or upload a CSV.</p></div>}
      </div>
    </div>
  );
}
