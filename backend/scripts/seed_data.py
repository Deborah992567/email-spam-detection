"""
Seed data script for development - contains sample emails (spam, ham).
These are clearly identified as SAMPLE data for development purposes.
Logs activity to the logs/ folder.
"""
import sys
import logging
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.core.logging_config import setup_logging
from backend.app.database.connection import SessionLocal
from backend.app.models.models import TrainingSample
from backend.app.utils.sample_data import SAMPLE_EMAILS

setup_logging()
logger = logging.getLogger("spamshield.scripts")


def seed():
    """Seed development sample data into the training_samples table."""
    db = SessionLocal()
    try:
        existing_count = db.query(TrainingSample).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} training samples. Skipping seed.")
            logger.info("Seed skipped - database already has %d samples", existing_count)
            return

        for item in SAMPLE_EMAILS:
            sample = TrainingSample(message=item["message"], label=item["label"], source="sample")
            db.add(sample)

        db.commit()
        spam = sum(1 for i in SAMPLE_EMAILS if i["label"] == "spam")
        ham = sum(1 for i in SAMPLE_EMAILS if i["label"] == "ham")
        print(f"Successfully seeded {len(SAMPLE_EMAILS)} development sample records ({spam} spam, {ham} ham).")
        print("NOTE: These are SAMPLE data for development/testing purposes only.")
        logger.info("Seeded %d sample records (%d spam, %d ham)", len(SAMPLE_EMAILS), spam, ham)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
