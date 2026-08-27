"""
Model management router for administrators.
"""
import sys
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db, SessionLocal
from backend.app.models.models import User, ModelVersion, TrainingSample
from backend.app.schemas.schemas import ModelVersionResponse, TrainingResultResponse
from backend.app.auth.auth import require_admin

router = APIRouter(prefix="/api/model", tags=["Model"])


@router.get("/versions")
def list_versions(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    versions = db.query(ModelVersion).order_by(ModelVersion.trained_at.desc()).all()
    return [ModelVersionResponse.model_validate(v) for v in versions]


@router.get("/current")
def get_current_model(
    admin: User = Depends(require_admin),
):
    from ml.models.model_manager import get_latest_version
    info = get_latest_version()
    if not info:
        return {"status": "no_model", "message": "No trained model found"}
    return info


@router.post("/train")
def train_model(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    samples = db.query(TrainingSample).all()
    if len(samples) < 10:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough training samples ({len(samples)}). Need at least 10.",
        )

    import pandas as pd
    data = [{"label": s.label, "message": s.message} for s in samples]
    df = pd.DataFrame(data)

    from ml.training.trainer import train_models
    results = train_models(df)

    # Reload model cache in predictor
    from ml.prediction.predictor import reload_model
    reload_model()

    best = results["results"][results["best_model"]]
    version = ModelVersion(
        version=results["best_version"],
        algorithm=results["best_model"],
        accuracy=best["accuracy"],
        precision=best["precision"],
        recall=best["recall"],
        f1_score=best["f1_score"],
    )
    db.add(version)
    db.commit()

    return TrainingResultResponse(
        best_model=results["best_model"],
        best_version=results["best_version"],
        results=results["results"],
        train_size=results["train_size"],
        test_size=results["test_size"],
        total_samples=results["total_samples"],
    )
