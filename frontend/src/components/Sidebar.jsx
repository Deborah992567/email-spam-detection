import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  DashboardIcon, MailIcon, HistoryIcon, UserIcon, LogOutIcon,
  ShieldIcon, MenuIcon, CloseIcon, UsersIcon, DatabaseIcon, BrainIcon,
  BarChartIcon
} from '../components/Icons';

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { to: '/dashboard', icon: <DashboardIcon size={20} />, label: 'Dashboard' },
    { to: '/analyze', icon: <MailIcon size={20} />, label: 'Analyze Email' },
    { to: '/history', icon: <HistoryIcon size={20} />, label: 'Analysis History' },
  ];

  const adminItems = user?.role === 'admin' ? [
    { to: '/admin', icon: <BarChartIcon size={20} />, label: 'Admin Dashboard' },
    { to: '/admin/users', icon: <UsersIcon size={20} />, label: 'User Management' },
    { to: '/admin/dataset', icon: <DatabaseIcon size={20} />, label: 'Dataset' },
    { to: '/admin/model', icon: <BrainIcon size={20} />, label: 'Model Performance' },
  ] : [];

  return (
    <>
      <button className="mobile-menu-btn" onClick={() => setOpen(!open)}>
        {open ? <CloseIcon size={24} /> : <MenuIcon size={24} />}
      </button>
      <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <ShieldIcon size={28} className="sidebar-logo-icon" />
          <span className="sidebar-logo-text">SpamShield</span>
        </div>

        <nav className="sidebar-nav">
          {navItems.map(item => (
            <NavLink key={item.to} to={item.to} className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`} onClick={() => setOpen(false)}>
              {item.icon}
              <span>{item.label}</span>
            </NavLink>
          ))}

          {adminItems.length > 0 && (
            <>
              <div className="sidebar-divider" />
              <span className="sidebar-section-title">Administration</span>
              {adminItems.map(item => (
                <NavLink key={item.to} to={item.to} className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`} onClick={() => setOpen(false)}>
                  {item.icon}
                  <span>{item.label}</span>
                </NavLink>
              ))}
            </>
          )}
        </nav>

        <div className="sidebar-footer">
          <NavLink to="/profile" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`} onClick={() => setOpen(false)}>
            <UserIcon size={20} />
            <span>{user?.name || 'Profile'}</span>
          </NavLink>
          <button className="sidebar-link logout-btn" onClick={handleLogout}>
            <LogOutIcon size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
      {open && <div className="sidebar-overlay" onClick={() => setOpen(false)} />}
    </>
  );
}
