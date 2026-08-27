import React from 'react';

export default function ConfirmDialog({ isOpen, title, message, onConfirm, onCancel }) {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" style={{ maxWidth: 400 }} onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{title || 'Confirm'}</h3>
        </div>
        <div className="modal-body">
          <p style={{ marginBottom: 20, color: 'var(--text-secondary)' }}>{message}</p>
          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
            <button className="btn btn-outline" onClick={onCancel}>Cancel</button>
            <button className="btn btn-danger" onClick={onConfirm}>Confirm</button>
          </div>
        </div>
      </div>
    </div>
  );
}
