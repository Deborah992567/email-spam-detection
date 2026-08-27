"""
Seed data script for development - contains sample emails (spam, ham).
These are clearly identified as SAMPLE data for development purposes.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.database.connection import SessionLocal
from backend.app.models.models import TrainingSample
from backend.app.utils.sample_data import SAMPLE_EMAILS


def seed():
    """Seed development sample data into the training_samples table."""
    db = SessionLocal()
    try:
        existing_count = db.query(TrainingSample).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} training samples. Skipping seed.")
            return

        for item in SAMPLE_EMAILS:
            sample = TrainingSample(message=item["message"], label=item["label"], source="sample")
            db.add(sample)

        db.commit()
        spam = sum(1 for i in SAMPLE_EMAILS if i["label"] == "spam")
        ham = sum(1 for i in SAMPLE_EMAILS if i["label"] == "ham")
        print(f"Successfully seeded {len(SAMPLE_EMAILS)} development sample records ({spam} spam, {ham} ham).")
        print("NOTE: These are SAMPLE data for development/testing purposes only.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
