import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { SearchIcon, FilterIcon, TrashIcon, ChevronRightIcon, MailIcon } from '../components/Icons';

export default function HistoryPage() {
  const [analyses, setAnalyses] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useEffect(() => { fetchHistory(); }, [page, filter]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const params = { page, per_page: 10 };
      if (search) params.search = search;
      if (filter) params.prediction = filter;
      const res = await api.get('/api/analysis/', { params });
      setAnalyses(res.data.items);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      addToast('Failed to load history', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchHistory();
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this analysis?')) return;
    try {
      await api.delete(`/api/analysis/${id}`);
      addToast('Analysis deleted', 'success');
      fetchHistory();
    } catch (err) {
      addToast('Failed to delete', 'error');
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Analysis History</h1>
        <span className="badge badge-outline">{total} total</span>
      </div>

      <div className="card">
        <div className="table-toolbar">
          <form onSubmit={handleSearch} className="search-form">
            <SearchIcon size={18} />
            <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search by sender, subject..." />
            <button type="submit" className="btn btn-sm btn-primary">Search</button>
          </form>
          <div className="filter-group">
            <FilterIcon size={16} />
            <select value={filter} onChange={e => { setFilter(e.target.value); setPage(1); }}>
              <option value="">All</option>
              <option value="spam">Spam Only</option>
              <option value="ham">Ham Only</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="page-loading"><div className="spinner" /></div>
        ) : analyses.length > 0 ? (
          <>
            <div className="table-responsive">
              <table className="table">
                <thead>
                  <tr>
                    <th>Subject</th>
                    <th>Sender</th>
                    <th>Result</th>
                    <th>Confidence</th>
                    <th>Risk</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {analyses.map(a => (
                    <tr key={a.id}>
                      <td className="text-truncate" style={{maxWidth: 180}}>{a.subject || 'No subject'}</td>
                      <td>{a.sender || 'Unknown'}</td>
                      <td>
                        <span className={`badge badge-${a.prediction === 'spam' ? 'danger' : 'success'}`}>
                          {a.prediction.toUpperCase()}
                        </span>
                      </td>
                      <td>{a.confidence}%</td>
                      <td><span className={`risk-badge risk-${a.risk_level}`}>{a.risk_level}</span></td>
                      <td>{new Date(a.created_at).toLocaleDateString()}</td>
                      <td className="actions-cell">
                        <Link to={`/history/${a.id}`} className="btn btn-sm btn-outline"><ChevronRightIcon size={14} /></Link>
                        <button className="btn btn-sm btn-danger" onClick={() => handleDelete(a.id)}><TrashIcon size={14} /></button>
                      </td>
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
        ) : (
          <div className="empty-state">
            <MailIcon size={48} />
            <p>No analysis history found.</p>
            <Link to="/analyze" className="btn btn-primary">Analyze Your First Email</Link>
          </div>
        )}
      </div>
    </div>
  );
}
