import React from 'react';
import { Link } from 'react-router-dom';
import { MailIcon } from './Icons';

export default function EmptyState({ icon, title, message, actionTo, actionLabel }) {
  return (
    <div className="empty-state">
      {icon || <MailIcon size={48} />}
      {title && <h3>{title}</h3>}
      <p>{message || 'No data available.'}</p>
      {actionTo && actionLabel && (
        <Link to={actionTo} className="btn btn-primary">{actionLabel}</Link>
      )}
    </div>
  );
}
