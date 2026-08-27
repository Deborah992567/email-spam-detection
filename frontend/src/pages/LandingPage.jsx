import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldIcon, MailIcon, BrainIcon, BarChartIcon, CheckCircleIcon } from '../components/Icons';

export default function LandingPage() {
  return (
    <div className="landing">
      <nav className="landing-nav">
        <div className="landing-nav-inner">
          <div className="landing-brand">
            <ShieldIcon size={28} />
            <span>SpamShield</span>
          </div>
          <div className="landing-nav-links">
            <Link to="/login" className="btn btn-outline">Login</Link>
            <Link to="/register" className="btn btn-primary">Get Started</Link>
          </div>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">AI-Powered Email Security</div>
          <h1>Intelligent Email Spam Detection</h1>
          <p>Protect your inbox with advanced machine learning. Analyze emails in real-time and get instant spam classification with detailed explanations.</p>
          <div className="hero-actions">
            <Link to="/register" className="btn btn-primary btn-lg">Start Analyzing</Link>
            <Link to="/login" className="btn btn-outline btn-lg">Sign In</Link>
          </div>
        </div>
      </section>

      <section className="features">
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon"><BrainIcon size={32} /></div>
            <h3>ML-Powered Detection</h3>
            <p>Advanced NLP pipeline with TF-IDF vectorization and multiple classifiers for accurate spam detection.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><MailIcon size={32} /></div>
            <h3>Instant Analysis</h3>
            <p>Get real-time classification results with confidence scores and detailed risk assessment.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><BarChartIcon size={32} /></div>
            <h3>Visual Dashboard</h3>
            <p>Track your analysis history with charts, statistics, and trend visualization.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"><ShieldIcon size={32} /></div>
            <h3>Explainable Results</h3>
            <p>Understand why an email was flagged with clear indicators and risk factors.</p>
          </div>
        </div>
      </section>

      <section className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Submit Email</h3>
            <p>Paste the email content, subject, and sender address.</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>AI Analysis</h3>
            <p>Our ML model analyzes the text using NLP techniques.</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Get Results</h3>
            <p>Receive classification, confidence score, and indicators.</p>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <p>SpamShield - AI-Powered Email Spam Detection System</p>
      </footer>
    </div>
  );
}
