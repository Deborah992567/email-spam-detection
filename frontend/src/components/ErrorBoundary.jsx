import React from 'react';
import { ShieldIcon } from './Icons';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Surface a console warning for debugging without crashing the UI
    console.error('SpamShield UI error:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-boundary-card">
            <div className="error-boundary-icon"><ShieldIcon size={36} className="auth-logo" /></div>
            <h2>Something went wrong</h2>
            <p>An unexpected error occurred while rendering this page.</p>
            <div className="error-boundary-actions">
              <button className="btn btn-primary" onClick={this.handleReset}>Try Again</button>
              <button className="btn btn-outline" onClick={() => { window.location.href = '/'; }}>Go Home</button>
            </div>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
