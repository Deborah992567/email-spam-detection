"""
Database initialization and admin user creation script.
Logs activity to the logs/ folder.
"""
import sys
import os
import logging
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.database.connection import engine, Base, SessionLocal
from backend.app.models.models import User
from backend.app.auth.auth import hash_password
from backend.app.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("spamshield.scripts")


def init_db():
    """Create all database tables."""
    print("Creating database tables...")
    logger.info("Creating database tables")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    logger.info("Database tables created successfully")


def create_admin(email: str, password: str, name: str = "Administrator"):
    """Create an admin user."""
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User with email {email} already exists.")
            logger.info("Admin user already exists with email %s", email)
            return

        admin = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role="admin",
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created: {email}")
        logger.info("Admin user created: %s", email)
    finally:
        db.close()


def create_test_user(email: str = "test@test.com", password: str = "test123"):
    """Create a test user."""
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User with email {email} already exists.")
            logger.info("Test user already exists with email %s", email)
            return

        user = User(
            name="Test User",
            email=email,
            password_hash=hash_password(password),
            role="user",
        )
        db.add(user)
        db.commit()
        print(f"Test user created: {email} / {password}")
        logger.info("Test user created with email %s", email)
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Database initialization")
    parser.add_argument("--admin-email", default="admin@spamdetect.com")
    parser.add_argument("--admin-password", default="admin123")
    parser.add_argument("--create-test-user", action="store_true")
    args = parser.parse_args()

    init_db()
    create_admin(args.admin_email, args.admin_password)
    if args.create_test_user:
        create_test_user()
    print("Done.")
    logger.info("Database initialization script finished")
