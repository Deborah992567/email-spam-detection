import React from 'react';
import { useToast } from '../context/ToastContext';
import { CheckCircleIcon, XCircleIcon, InfoIcon, AlertTriangleIcon, CloseIcon } from './Icons';

const iconMap = {
  success: <CheckCircleIcon size={18} />,
  error: <XCircleIcon size={18} />,
  info: <InfoIcon size={18} />,
  warning: <AlertTriangleIcon size={18} />,
};

const colorMap = {
  success: 'var(--color-success)',
  error: 'var(--color-error)',
  info: 'var(--color-primary)',
  warning: 'var(--color-warning)',
};

export default function Toast() {
  const { toasts, removeToast } = useToast();

  return (
    <div className="toast-container">
      {toasts.map(toast => (
        <div key={toast.id} className="toast" style={{ borderLeftColor: colorMap[toast.type] || colorMap.info }}>
          <span className="toast-icon" style={{ color: colorMap[toast.type] }}>
            {iconMap[toast.type] || iconMap.info}
          </span>
          <span className="toast-message">{toast.message}</span>
          <button className="toast-close" onClick={() => removeToast(toast.id)}>
            <CloseIcon size={14} />
          </button>
        </div>
      ))}
    </div>
  );
}
