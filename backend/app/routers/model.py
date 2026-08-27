"""
Model management router - Train, evaluate, and manage ML models.
Requires admin role for all endpoints.
"""
import sys
import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db, SessionLocal
from backend.app.models.models import User, ModelVersion, TrainingSample
from backend.app.schemas.schemas import ModelVersionResponse, TrainingResultResponse
from backend.app.auth.auth import require_admin

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/model", tags=["Model"])


@router.get("/versions")
def list_versions(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    versions = db.query(ModelVersion).order_by(ModelVersion.trained_at.desc()).all()
    return [ModelVersionResponse.model_validate(v) for v in versions]


@router.get("/dataset-status")
def dataset_status(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    from backend.app.utils.sample_data import SAMPLE_EMAILS

    total = db.query(TrainingSample).count()
    spam = db.query(TrainingSample).filter(TrainingSample.label == "spam").count()
    ham = db.query(TrainingSample).filter(TrainingSample.label == "ham").count()
    return {
        "total": total,
        "spam": spam,
        "ham": ham,
        "enough_to_train": total >= 10 and spam > 0 and ham > 0,
        "source": "sample" if total <= len(SAMPLE_EMAILS) else "dataset",
    }


@router.post("/seed-sample-data")
def seed_sample_data(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    from backend.app.utils.sample_data import SAMPLE_EMAILS

    existing = db.query(TrainingSample).count()
    seeded = 0
    for item in SAMPLE_EMAILS:
        exists = db.query(TrainingSample).filter(
            TrainingSample.message == item["message"]
        ).first()
        if not exists:
            db.add(TrainingSample(
                message=item["message"],
                label=item["label"],
                source="sample",
            ))
            seeded += 1
    db.commit()
    return {
        "seeded": seeded,
        "skipped": len(SAMPLE_EMAILS) - seeded,
        "total_before": existing,
        "total_now": db.query(TrainingSample).count(),
        "note": "Seeded clearly-labeled SAMPLE data for development. Replace with a real dataset for production use.",
    }


@router.post("/seed-and-train")
def seed_and_train(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    from backend.app.utils.sample_data import SAMPLE_EMAILS

    seeded = 0
    for item in SAMPLE_EMAILS:
        exists = db.query(TrainingSample).filter(
            TrainingSample.message == item["message"]
        ).first()
        if not exists:
            db.add(TrainingSample(message=item["message"], label=item["label"], source="sample"))
            seeded += 1
    db.commit()

    samples = db.query(TrainingSample).all()
    labels = {s.label for s in samples}
    if len(samples) < 10 or labels != {"spam", "ham"}:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough varied samples ({len(samples)}) to train.",
        )

    import pandas as pd
    data = [{"label": s.label, "message": s.message} for s in samples]
    df = pd.DataFrame(data)

    try:
        from ml.training.trainer import train_models
        results = train_models(df)
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

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

    return {
        "seeded": seeded,
        "total_samples": results["total_samples"],
        "best_model": results["best_model"],
        "best_version": results["best_version"],
        "metrics": {
            "accuracy": best["accuracy"],
            "precision": best["precision"],
            "recall": best["recall"],
            "f1_score": best["f1_score"],
        },
        "note": "Model trained on clearly-labeled SAMPLE data for development.",
    }


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

    # Check both classes present
    labels = {s.label for s in samples}
    if labels != {"spam", "ham"}:
        raise HTTPException(
            status_code=400,
            detail=f"Dataset must contain both 'spam' and 'ham' samples. Found: {labels}",
        )

    import pandas as pd
    data = [{"label": s.label, "message": s.message} for s in samples]
    df = pd.DataFrame(data)

    logger.info(f"Training model with {len(samples)} samples")

    try:
        from ml.training.trainer import train_models
        results = train_models(df)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

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
    logger.info(f"Model trained successfully: {results['best_model']} ({results['best_version']})")

    return TrainingResultResponse(
        best_model=results["best_model"],
        best_version=results["best_version"],
        results=results["results"],
        train_size=results["train_size"],
        test_size=results["test_size"],
        total_samples=results["total_samples"],
    )
