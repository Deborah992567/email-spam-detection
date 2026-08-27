import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { SearchIcon, TrashIcon, UsersIcon } from '../components/Icons';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { Skeleton } from '../components/Skeleton';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);

  useDocumentTitle('User Management');
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useEffect(() => { fetchUsers(); }, [page]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const params = { page, per_page: 10 };
      if (search) params.search = search;
      const res = await api.get('/api/admin/users', { params });
      setUsers(res.data.items);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      addToast('Failed to load users', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchUsers();
  };

  const handleDelete = async (id, name) => {
    if (!confirm(`Delete user "${name}"? This will also delete all their analyses.`)) return;
    try {
      await api.delete(`/api/admin/users/${id}`);
      addToast('User deleted', 'success');
      fetchUsers();
    } catch (err) {
      addToast(err.response?.data?.detail || 'Failed to delete user', 'error');
    }
  };

  return (
    <div className="page">
      <div className="page-header"><h1>User Management</h1><span className="badge badge-outline">{total} users</span></div>
      <div className="card">
        <div className="table-toolbar">
          <form onSubmit={handleSearch} className="search-form">
            <SearchIcon size={18} />
            <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search users..." />
            <button type="submit" className="btn btn-sm btn-primary">Search</button>
          </form>
        </div>
        {loading ? (
          <div style={{ padding: '4px 0' }}>
            <Skeleton height={40} style={{ marginBottom: 12, borderRadius: 8 }} />
            <Skeleton height={40} style={{ marginBottom: 12, borderRadius: 8 }} />
            <Skeleton height={40} style={{ marginBottom: 12, borderRadius: 8 }} />
            <Skeleton height={40} style={{ borderRadius: 8 }} />
          </div>
        ) : users.length > 0 ? (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr><th>Name</th><th>Email</th><th>Role</th><th>Joined</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id}>
                    <td>{u.name}</td>
                    <td>{u.email}</td>
                    <td><span className={`badge badge-${u.role === 'admin' ? 'warning' : 'info'}`}>{u.role}</span></td>
                    <td>{new Date(u.created_at).toLocaleDateString()}</td>
                    <td>
                      <button className="btn btn-sm btn-danger" onClick={() => handleDelete(u.id, u.name)}><TrashIcon size={14} /></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <div className="empty-state"><UsersIcon size={48} /><p>No users found.</p></div>}
        <div className="pagination">
          <button className="btn btn-sm btn-outline" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Prev</button>
          <span>Page {page} of {pages}</span>
          <button className="btn btn-sm btn-outline" disabled={page >= pages} onClick={() => setPage(p => p + 1)}>Next</button>
        </div>
      </div>
    </div>
  );
}
