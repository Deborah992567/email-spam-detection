"""
Dataset management router for administrators.
"""
import io
import csv
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database.connection import get_db
from backend.app.models.models import User, TrainingSample
from backend.app.schemas.schemas import (
    TrainingSampleCreate, TrainingSampleResponse, TrainingSampleListResponse
)
from backend.app.auth.auth import require_admin

router = APIRouter(prefix="/api/dataset", tags=["Dataset"])


@router.get("/", response_model=TrainingSampleListResponse)
def list_samples(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    label: Optional[str] = None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(TrainingSample)

    if search:
        query = query.filter(TrainingSample.message.ilike(f"%{search}%"))
    if label and label in ("spam", "ham"):
        query = query.filter(TrainingSample.label == label)

    total = query.count()
    items = query.order_by(TrainingSample.created_at.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    return TrainingSampleListResponse(
        items=[TrainingSampleResponse.model_validate(s) for s in items],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
    )


@router.get("/stats")
def dataset_stats(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    total = db.query(TrainingSample).count()
    spam = db.query(TrainingSample).filter(TrainingSample.label == "spam").count()
    ham = db.query(TrainingSample).filter(TrainingSample.label == "ham").count()
    return {"total": total, "spam": spam, "ham": ham}


@router.post("/", response_model=TrainingSampleResponse, status_code=201)
def add_sample(
    data: TrainingSampleCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    sample = TrainingSample(message=data.message, label=data.label)
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return TrainingSampleResponse.model_validate(sample)


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text))
    fieldnames_lower = {f.lower().strip(): f for f in (reader.fieldnames or [])}

    label_col = None
    text_col = None
    for alias in ["label", "category", "class"]:
        if alias in fieldnames_lower:
            label_col = fieldnames_lower[alias]
            break
    for alias in ["message", "text", "email", "content", "body"]:
        if alias in fieldnames_lower:
            text_col = fieldnames_lower[alias]
            break

    if not label_col or not text_col:
        raise HTTPException(
            status_code=400,
            detail=f"CSV must have 'label' and 'message' columns. Found: {list(reader.fieldnames or [])}",
        )

    added = 0
    skipped = 0
    label_map = {"spam": "spam", "ham": "ham", "1": "spam", "0": "ham"}

    for row in reader:
        raw_label = row.get(label_col, "").strip().lower()
        label = label_map.get(raw_label)
        if not label:
            skipped += 1
            continue

        message = row.get(text_col, "").strip()
        if not message:
            skipped += 1
            continue

        sample = TrainingSample(message=message, label=label)
        db.add(sample)
        added += 1

    db.commit()
    return {"message": f"Dataset uploaded. Added {added} samples, skipped {skipped}."}


@router.post("/bulk", status_code=201)
def bulk_add_samples(
    samples: list[TrainingSampleCreate],
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    added = 0
    for s in samples:
        sample = TrainingSample(message=s.message, label=s.label)
        db.add(sample)
        added += 1
    db.commit()
    return {"message": f"Added {added} samples"}


@router.delete("/{sample_id}")
def delete_sample(
    sample_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    sample = db.query(TrainingSample).filter(TrainingSample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    db.delete(sample)
    db.commit()
    return {"message": "Sample deleted successfully"}
