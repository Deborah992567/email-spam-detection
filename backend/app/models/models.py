"""
Database models (SQLAlchemy ORM).
"""
from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime,
    ForeignKey, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analyses = relationship("EmailAnalysis", back_populates="user", cascade="all, delete-orphan")


class EmailAnalysis(Base):
    __tablename__ = "email_analyses"
    __table_args__ = (
        Index("idx_analysis_user_id", "user_id"),
        Index("idx_analysis_prediction", "prediction"),
        Index("idx_analysis_created_at", "created_at"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(255), nullable=True)
    subject = Column(String(500), nullable=True)
    body = Column(Text, nullable=False)
    prediction = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    indicators = Column(Text, nullable=True)
    model_version = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="analyses")


class TrainingSample(Base):
    __tablename__ = "training_samples"
    __table_args__ = (
        Index("idx_sample_label", "label"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(Text, nullable=False)
    label = Column(String(10), nullable=False)
    source = Column(String(20), default="dataset", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version = Column(String(50), unique=True, nullable=False)
    algorithm = Column(String(100), nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    trained_at = Column(DateTime(timezone=True), server_default=func.now())
