import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldIcon, ArrowLeftIcon } from '../components/Icons';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function NotFoundPage() {
  useDocumentTitle('Page Not Found');

  return (
    <div className="not-found-page">
      <div className="not-found-card">
        <div className="not-found-code">404</div>
        <div className="not-found-icon"><ShieldIcon size={40} className="auth-logo" /></div>
        <h1>Page Not Found</h1>
        <p>The page you're looking for does not exist or has been moved.</p>
        <Link to="/" className="btn btn-primary">
          <ArrowLeftIcon size={16} /> Back to Home
        </Link>
      </div>
    </div>
  );
}
