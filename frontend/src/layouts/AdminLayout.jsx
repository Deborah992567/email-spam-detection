import React from 'react';
import Sidebar from '../components/Sidebar';

export default function AdminLayout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}
