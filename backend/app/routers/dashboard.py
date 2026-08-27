"""
Dashboard statistics router - aggregate stats, trends, and risk distribution.
"""
import json
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from backend.app.database.connection import get_db
from backend.app.models.models import User, EmailAnalysis
from backend.app.schemas.schemas import DashboardStats, AnalysisResponse
from backend.app.auth.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


def _analysis_to_dict(a: EmailAnalysis) -> dict:
    resp = AnalysisResponse.model_validate(a)
    resp.indicators = json.loads(a.indicators) if a.indicators else None
    return resp.model_dump()


@router.get("/", response_model=DashboardStats, summary="Get user dashboard statistics")
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(EmailAnalysis).filter(EmailAnalysis.user_id == current_user.id)

    total = query.count()
    spam_count = query.filter(EmailAnalysis.prediction == "spam").count()
    ham_count = total - spam_count
    spam_pct = round((spam_count / total * 100) if total > 0 else 0, 1)

    recent = query.order_by(EmailAnalysis.created_at.desc()).limit(6).all()
    recent_items = [_analysis_to_dict(a) for a in recent]

    # Risk distribution
    risk_counts = {
        "high": query.filter(EmailAnalysis.risk_level == "high").count(),
        "medium": query.filter(EmailAnalysis.risk_level == "medium").count(),
        "low": query.filter(EmailAnalysis.risk_level == "low").count(),
    }

    # Last 30 days activity
    daily = []
    for i in range(29, -1, -1):
        day = (datetime.now(timezone.utc).date() - timedelta(days=i))
        day_start = datetime.combine(day, datetime.min.time()).replace(tzinfo=timezone.utc)
        day_end = day_start + timedelta(days=1)
        day_total = query.filter(
            EmailAnalysis.created_at >= day_start,
            EmailAnalysis.created_at < day_end,
        ).count()
        day_spam = query.filter(
            EmailAnalysis.created_at >= day_start,
            EmailAnalysis.created_at < day_end,
            EmailAnalysis.prediction == "spam",
        ).count()
        daily.append({
            "date": day.isoformat(),
            "total": day_total,
            "spam": day_spam,
            "ham": day_total - day_spam,
        })

    return DashboardStats(
        total_analyses=total,
        spam_count=spam_count,
        ham_count=ham_count,
        spam_percentage=spam_pct,
        recent_analyses=recent_items,
        daily_stats=daily,
        risk_distribution=risk_counts,
    )
