import React from 'react';

export default function Skeleton({ type = 'text', width = '100%', height = 14, style }) {
  return (
    <div
      className={`skeleton skeleton-${type}`}
      style={{ width, height, ...style }}
    />
  );
}

export function StatsSkeleton({ count = 4 }) {
  return (
    <div className="stats-grid">
      {Array.from({ length: count }).map((_, i) => (
        <div className="stat-card" key={i}>
          <div className="skeleton skeleton-circle" style={{ width: 48, height: 48 }} />
          <div className="stat-info" style={{ flex: 1 }}>
            <Skeleton width="60%" height={24} />
            <Skeleton width="40%" height={12} style={{ marginTop: 8 }} />
          </div>
        </div>
      ))}
    </div>
  );
}

export function ChartSkeleton({ height = 260 }) {
  return (
    <div className="chart-card">
      <Skeleton width="180px" height={18} />
      <div className="skeleton skeleton-block" style={{ height, marginTop: 16 }} />
    </div>
  );
}

export function TableSkeleton({ rows = 5 }) {
  return (
    <div className="card">
      {Array.from({ length: rows }).map((_, i) => (
        <Skeleton key={i} height={36} style={{ marginBottom: 12, borderRadius: 8 }} />
      ))}
    </div>
  );
}
