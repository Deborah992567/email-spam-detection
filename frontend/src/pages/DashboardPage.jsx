import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { ShieldIcon, MailIcon, AlertTriangleIcon, CheckCircleIcon, ChevronRightIcon } from '../components/Icons';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, AreaChart, Area } from 'recharts';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { StatsSkeleton, ChartSkeleton, TableSkeleton } from '../components/Skeleton';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useDocumentTitle('Dashboard');

  useEffect(() => { fetchStats(); }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get('/api/dashboard/');
      setStats(res.data);
    } catch (err) {
      addToast('Failed to load dashboard data', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page">
        <div className="page-header"><h1>Dashboard</h1></div>
        <StatsSkeleton />
        <div className="charts-grid">
          <ChartSkeleton />
          <ChartSkeleton />
        </div>
        <ChartSkeleton />
        <TableSkeleton rows={4} />
      </div>
    );
  }
  if (!stats) return <div className="empty-state"><p>Failed to load dashboard.</p></div>;

  const pieData = [
    { name: 'Spam', value: stats.spam_count || 0 },
    { name: 'Ham', value: stats.ham_count || 0 },
  ];
  const COLORS = ['#ef4444', '#22c55e'];

  const riskData = stats.risk_distribution ? [
    { name: 'High', value: stats.risk_distribution.high || 0 },
    { name: 'Medium', value: stats.risk_distribution.medium || 0 },
    { name: 'Low', value: stats.risk_distribution.low || 0 },
  ].filter(d => d.value > 0) : [];
  const RISK_COLORS = ['#ef4444', '#f59e0b', '#22c55e'];

  const trendData = stats.daily_stats || [];

  return (
    <div className="page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <Link to="/analyze" className="btn btn-primary">
          <MailIcon size={18} /> Analyze Email
        </Link>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon stat-icon-blue"><MailIcon size={26} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.total_analyses}</span>
            <span className="stat-label">Total Analyzed</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-red"><AlertTriangleIcon size={26} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.spam_count}</span>
            <span className="stat-label">Spam Detected</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-green"><CheckCircleIcon size={26} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.ham_count}</span>
            <span className="stat-label">Legitimate</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon stat-icon-purple"><ShieldIcon size={26} /></div>
          <div className="stat-info">
            <span className="stat-value">{stats.spam_percentage}%</span>
            <span className="stat-label">Spam Rate</span>
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Spam vs Ham Distribution</h3>
          {stats.total_analyses > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={62} outerRadius={92} paddingAngle={5} dataKey="value">
                  {pieData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-light)', borderRadius: 8 }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state"><p>No data yet</p></div>
          )}
        </div>

        <div className="chart-card">
          <h3>Risk Level Distribution</h3>
          {riskData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={riskData} cx="50%" cy="50%" innerRadius={62} outerRadius={92} paddingAngle={5} dataKey="value">
                  {riskData.map((_, index) => (
                    <Cell key={index} fill={RISK_COLORS[index]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-light)', borderRadius: 8 }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state"><p>No risk data yet</p></div>
          )}
        </div>
      </div>

      <div className="chart-card">
        <h3>Analysis Trend (Last 30 Days)</h3>
        {trendData.some(d => d.total > 0) ? (
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="spamGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.6} />
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="hamGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#22c55e" stopOpacity={0.6} />
                  <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="date" tick={{ fontSize: 10, fill: 'var(--text-muted)' }} />
              <YAxis tick={{ fontSize: 10, fill: 'var(--text-muted)' }} />
              <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-light)', borderRadius: 8 }} />
              <Legend />
              <Area type="monotone" dataKey="spam" stroke="#ef4444" fill="url(#spamGrad)" name="Spam" />
              <Area type="monotone" dataKey="ham" stroke="#22c55e" fill="url(#hamGrad)" name="Ham" />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="empty-state"><p>No activity data yet</p></div>
        )}
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Recent Analyses</h3>
          <Link to="/history" className="btn btn-sm btn-outline">View All <ChevronRightIcon size={14} /></Link>
        </div>
        {stats.recent_analyses && stats.recent_analyses.length > 0 ? (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Sender</th>
                  <th>Result</th>
                  <th>Confidence</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_analyses.map(a => (
                  <tr key={a.id}>
                    <td className="text-truncate" style={{maxWidth: 200}}>{a.subject || 'No subject'}</td>
                    <td>{a.sender || 'Unknown'}</td>
                    <td>
                      <span className={`badge badge-${a.prediction === 'spam' ? 'danger' : 'success'}`}>
                        {a.prediction === 'spam' ? 'SPAM' : 'HAM'}
                      </span>
                    </td>
                    <td>{a.confidence}%</td>
                    <td>{new Date(a.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <MailIcon size={48} />
            <p>No analyses yet. <Link to="/analyze">Analyze your first email</Link></p>
          </div>
        )}
      </div>
    </div>
  );
}
