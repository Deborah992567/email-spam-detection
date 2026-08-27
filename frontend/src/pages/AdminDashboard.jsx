import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { UsersIcon, MailIcon, AlertTriangleIcon, CheckCircleIcon, DatabaseIcon, BrainIcon } from '../components/Icons';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useDocumentTitle('Admin Dashboard');

  useEffect(() => { fetchStats(); }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get('/api/admin/stats');
      setStats(res.data);
    } catch (err) {
      addToast('Failed to load admin stats', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page-loading"><div className="spinner" /></div>;
  if (!stats) return <div className="empty-state"><p>Failed to load stats.</p></div>;

  const pieData = [
    { name: 'Spam', value: stats.spam_count || 0 },
    { name: 'Ham', value: stats.ham_count || 0 },
  ];
  const COLORS = ['#ef4444', '#22c55e'];

  return (
    <div className="page">
      <div className="page-header"><h1>Admin Dashboard</h1></div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon stat-icon-blue"><UsersIcon size={24} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.total_users}</span>
            <span className="stat-label">Users</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-purple"><MailIcon size={24} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.total_analyses}</span>
            <span className="stat-label">Total Analyses</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-red"><AlertTriangleIcon size={24} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.spam_count}</span>
            <span className="stat-label">Spam Detected</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-green"><CheckCircleIcon size={24} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.ham_count}</span>
            <span className="stat-label">Legitimate</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-orange"><DatabaseIcon size={24} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.training_samples}</span>
            <span className="stat-label">Training Samples</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-teal"><BrainIcon size={24} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.model_versions}</span>
            <span className="stat-label">Model Versions</span>
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Spam Distribution</h3>
          {stats.total_analyses > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={5} dataKey="value">
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : <div className="empty-state"><p>No data</p></div>}
        </div>
        <div className="chart-card">
          <h3>Quick Actions</h3>
          <div className="quick-actions">
            <Link to="/admin/users" className="quick-action"><UsersIcon size={24} /><span>Manage Users</span></Link>
            <Link to="/admin/dataset" className="quick-action"><DatabaseIcon size={24} /><span>Dataset</span></Link>
            <Link to="/admin/model" className="quick-action"><BrainIcon size={24} /><span>Model Perf.</span></Link>
          </div>
        </div>
      </div>
    </div>
  );
}
