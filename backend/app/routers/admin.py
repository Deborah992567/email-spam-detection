"""
Admin router for user management, system stats, and administration.
"""
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from backend.app.database.connection import get_db
from backend.app.models.models import User, EmailAnalysis, TrainingSample, ModelVersion
from backend.app.schemas.schemas import (
    UserResponse, AnalysisResponse, AnalysisListResponse,
    AdminStats, PaginatedResponse, TrainingSampleResponse
)
from backend.app.auth.auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminStats)
def get_admin_stats(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return AdminStats(
        total_users=db.query(User).count(),
        total_analyses=db.query(EmailAnalysis).count(),
        spam_count=db.query(EmailAnalysis).filter(EmailAnalysis.prediction == "spam").count(),
        ham_count=db.query(EmailAnalysis).filter(EmailAnalysis.prediction == "ham").count(),
        spam_percentage=round(
            db.query(EmailAnalysis).filter(EmailAnalysis.prediction == "spam").count()
            / max(db.query(EmailAnalysis).count(), 1) * 100, 1
        ),
        model_versions=db.query(ModelVersion).count(),
        training_samples=db.query(TrainingSample).count(),
    )


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (User.name.ilike(search_filter)) | (User.email.ilike(search_filter))
        )

    total = query.count()
    users = query.order_by(User.created_at.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    return {
        "items": [UserResponse.model_validate(u) for u in users],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.get("/analyses")
def list_all_analyses(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    prediction: Optional[str] = None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(EmailAnalysis)

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

    return {
        "items": [
            {**AnalysisResponse.model_validate(a).model_dump(), "indicators": json.loads(a.indicators) if a.indicators else None}
            for a in items
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


@router.delete("/analyses/{analysis_id}")
def admin_delete_analysis(
    analysis_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    analysis = db.query(EmailAnalysis).filter(EmailAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    db.delete(analysis)
    db.commit()
    return {"message": "Analysis deleted successfully"}


@router.get("/model-versions")
def list_model_versions(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    versions = db.query(ModelVersion).order_by(ModelVersion.trained_at.desc()).all()
    return [ModelVersion.model_validate(v) for v in versions]
