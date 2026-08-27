import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { UserIcon, MailIcon, AlertTriangleIcon, CheckCircleIcon } from '../components/Icons';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [stats, setStats] = useState(null);

  useDocumentTitle('Profile');
  const [loading, setLoading] = useState(false);
  const { addToast } = useToast();

  useEffect(() => {
    if (user) {
      setName(user.name);
      setEmail(user.email);
    }
    fetchStats();
  }, [user]);

  const fetchStats = async () => {
    try {
      const res = await api.get('/api/users/me/stats');
      setStats(res.data);
    } catch (err) {
      /* non-critical */
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.put('/api/users/me', { name, email });
      updateUser(res.data);
      addToast('Profile updated', 'success');
    } catch (err) {
      addToast(err.response?.data?.detail || 'Update failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header"><h1>Profile</h1></div>

      {stats && (
        <div className="stats-grid stats-grid-3 profile-stats">
          <div className="stat-card">
            <div className="stat-icon stat-icon-purple"><MailIcon size={24} /></div>
            <div className="stat-info"><span className="stat-value">{stats.total}</span><span className="stat-label">My Analyses</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon stat-icon-red"><AlertTriangleIcon size={24} /></div>
            <div className="stat-info"><span className="stat-value">{stats.spam}</span><span className="stat-label">Spam Detected</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon stat-icon-green"><CheckCircleIcon size={24} /></div>
            <div className="stat-info"><span className="stat-value">{stats.ham}</span><span className="stat-label">Legitimate</span></div>
          </div>
        </div>
      )}

      <div className="card" style={{ maxWidth: 500 }}>
        <div className="profile-avatar"><UserIcon size={48} /></div>
        <form onSubmit={handleUpdate}>
          <div className="form-group">
            <label>Full Name</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} required minLength={2} />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Role</label>
            <input type="text" value={user?.role || ''} disabled className="input-disabled" />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Saving...' : 'Save Changes'}
          </button>
        </form>
      </div>
    </div>
  );
}
