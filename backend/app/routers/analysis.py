"""
Email analysis router - Analyze emails and get spam/ham predictions.
"""
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database.connection import get_db
from backend.app.models.models import User, EmailAnalysis
from backend.app.schemas.schemas import (
    AnalysisRequest, AnalysisResponse, AnalysisListResponse
)
from backend.app.auth.auth import get_current_user
from ml.prediction.predictor import predict_email

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.post("/", response_model=AnalysisResponse, status_code=201)
def analyze_email(
    data: AnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = predict_email(
        sender=data.sender or "unknown",
        subject=data.subject or "",
        body=data.body,
    )

    analysis = EmailAnalysis(
        user_id=current_user.id,
        sender=data.sender,
        subject=data.subject,
        body=data.body,
        prediction=result["prediction"],
        confidence=result["confidence"],
        risk_level=result["risk_level"],
        indicators=json.dumps(result["indicators"]),
        model_version=result.get("model_version"),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    response = AnalysisResponse.model_validate(analysis)
    response.indicators = result["indicators"]
    return response


@router.get("/", response_model=AnalysisListResponse)
def list_analyses(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    prediction: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|confidence|risk_level)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(EmailAnalysis).filter(EmailAnalysis.user_id == current_user.id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (EmailAnalysis.sender.ilike(search_filter)) |
            (EmailAnalysis.subject.ilike(search_filter)) |
            (EmailAnalysis.body.ilike(search_filter))
        )

    if prediction and prediction in ("spam", "ham"):
        query = query.filter(EmailAnalysis.prediction == prediction)

    total = query.count()

    sort_col = getattr(EmailAnalysis, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_col.desc())
    else:
        query = query.order_by(sort_col.asc())

    items = query.offset((page - 1) * per_page).limit(per_page).all()

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


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = db.query(EmailAnalysis).filter(
        EmailAnalysis.id == analysis_id,
        EmailAnalysis.user_id == current_user.id,
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    response = AnalysisResponse.model_validate(analysis)
    response.indicators = json.loads(analysis.indicators) if analysis.indicators else None
    return response


@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = db.query(EmailAnalysis).filter(
        EmailAnalysis.id == analysis_id,
        EmailAnalysis.user_id == current_user.id,
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    db.delete(analysis)
    db.commit()
    return {"message": "Analysis deleted successfully"}
