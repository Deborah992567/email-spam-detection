"""
History router - alias for analysis list with history-specific behavior.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timedelta, timezone
from backend.app.database.connection import get_db
from backend.app.models.models import User, EmailAnalysis
from backend.app.schemas.schemas import AnalysisListResponse, AnalysisResponse, DashboardStats
from backend.app.auth.auth import get_current_user
import json

router = APIRouter(prefix="/api/history", tags=["History"])


@router.get("/", response_model=AnalysisListResponse)
def get_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    prediction: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(EmailAnalysis).filter(EmailAnalysis.user_id == current_user.id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (EmailAnalysis.sender.ilike(search_filter)) |
            (EmailAnalysis.subject.ilike(search_filter))
        )

    if prediction and prediction in ("spam", "ham"):
        query = query.filter(EmailAnalysis.prediction == prediction)

    total = query.count()
    items = query.order_by(EmailAnalysis.created_at.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    response_items = []
    for a in items:
        resp = AnalysisResponse.model_validate(a)
        resp.indicators = json.loads(a.indicators) if a.indicators else None
        response_items.append(resp.model_dump())

    return AnalysisListResponse(
        items=response_items,
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
    )


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_analyses = db.query(EmailAnalysis).filter(EmailAnalysis.user_id == current_user.id)

    total = user_analyses.count()
    spam_count = user_analyses.filter(EmailAnalysis.prediction == "spam").count()
    ham_count = total - spam_count
    spam_pct = round((spam_count / total * 100) if total > 0 else 0, 1)

    recent = user_analyses.order_by(EmailAnalysis.created_at.desc()).limit(5).all()
    recent_items = []
    for a in recent:
        resp = AnalysisResponse.model_validate(a)
        resp.indicators = json.loads(a.indicators) if a.indicators else None
        recent_items.append(resp.model_dump())

    daily = []
    for i in range(6, -1, -1):
        day = datetime.now(timezone.utc).date() - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time()).replace(tzinfo=timezone.utc)
        day_end = day_start + timedelta(days=1)
        day_total = user_analyses.filter(
            EmailAnalysis.created_at >= day_start,
            EmailAnalysis.created_at < day_end,
        ).count()
        day_spam = user_analyses.filter(
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
    )
