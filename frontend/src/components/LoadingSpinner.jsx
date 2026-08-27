import React from 'react';

export default function LoadingSpinner({ size = 36, text = '' }) {
  return (
    <div className="page-loading">
      <div className="spinner" style={{ width: size, height: size }} />
      {text && <p style={{ marginTop: 12, color: 'var(--text-secondary)', fontSize: 14 }}>{text}</p>}
    </div>
  );
}
