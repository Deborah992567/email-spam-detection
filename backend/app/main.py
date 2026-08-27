"""
Email Spam Detection System - FastAPI Application
"""
import sys
import os
from pathlib import Path

# Add project root to path for ML imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.database.connection import engine, Base
from backend.app.routers import auth, users, analysis, history, admin, dataset, model, dashboard

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered email spam detection system with ML classification.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(analysis.router)
app.include_router(history.router)
app.include_router(dashboard.router)
app.include_router(admin.router)
app.include_router(dataset.router)
app.include_router(model.router)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}
