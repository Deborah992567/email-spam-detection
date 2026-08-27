"""
Dataset management router - Upload, add, and manage training samples.
Requires admin role for all endpoints.
"""
import io
import csv
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database.connection import get_db
from backend.app.models.models import User, TrainingSample
from backend.app.schemas.schemas import (
    TrainingSampleCreate, TrainingSampleResponse, TrainingSampleListResponse
)
from backend.app.auth.auth import require_admin

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/dataset", tags=["Dataset"])


@router.get("/template")
def csv_template(
    admin: User = Depends(require_admin),
):
    """Download a CSV template showing the expected format."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["label", "message"])
    writer.writeheader()
    writer.writerow({"label": "spam", "message": "Example spam email text goes here..."})
    writer.writerow({"label": "ham", "message": "Example legitimate email text goes here..."})
    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=dataset_template.csv"}
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers=headers,
    )


@router.get("/export")
def export_dataset(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Export all training samples as a CSV download."""
    samples = db.query(TrainingSample).order_by(TrainingSample.id).all()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "label", "source", "message", "created_at"])
    writer.writeheader()
    for s in samples:
        writer.writerow({
            "id": s.id,
            "label": s.label,
            "source": s.source,
            "message": s.message,
            "created_at": s.created_at.isoformat() if s.created_at else "",
        })
    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=training_dataset.csv"}
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers=headers,
    )


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
    sample_count = db.query(TrainingSample).filter(TrainingSample.source == "sample").count()
    dataset_count = db.query(TrainingSample).filter(TrainingSample.source == "dataset").count()
    return {
        "total": total,
        "spam": spam,
        "ham": ham,
        "source": {
            "sample": sample_count,
            "dataset": dataset_count,
        },
        "source_label": "sample" if total > 0 and sample_count >= dataset_count else "dataset",
    }


@router.post("/", response_model=TrainingSampleResponse, status_code=201)
def add_sample(
    data: TrainingSampleCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    sample = TrainingSample(message=data.message, label=data.label, source="dataset")
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
    label_map = {"spam": "spam", "ham": "ham", "1": "spam", "0": "ham", "true": "spam", "false": "ham", "yes": "spam", "no": "ham"}

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

        sample = TrainingSample(message=message, label=label, source="dataset")
        db.add(sample)
        added += 1

    db.commit()
    logger.info(f"Dataset uploaded: {added} samples added, {skipped} skipped")
    return {"message": f"Dataset uploaded successfully. Added {added} samples, skipped {skipped}."}


@router.post("/bulk", status_code=201)
def bulk_add_samples(
    samples: list[TrainingSampleCreate],
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    added = 0
    for s in samples:
        sample = TrainingSample(message=s.message, label=s.label, source="dataset")
        db.add(sample)
        added += 1
    db.commit()
    return {"message": f"Added {added} samples"}


@router.delete("/clear-all", summary="Delete all training samples")
def clear_all_samples(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    count = db.query(TrainingSample).count()
    db.query(TrainingSample).delete()
    db.commit()
    return {"message": f"Cleared all {count} training samples"}


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
