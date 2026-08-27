"""
SpamShield - Email Spam Detection System
FastAPI Application
"""
import sys
import os
import time
import logging
from pathlib import Path

# Add project root to path for ML imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.core.config import settings
from backend.app.core.logging_config import (
    setup_logging,
    make_http_request_logger,
    log_current_boot,
)
from backend.app.database.connection import engine, Base
from backend.app.routers import auth, users, analysis, history, admin, dataset, model, dashboard

# Logs are written to rotating files under the logs/ folder
setup_logging(log_to_console=settings.DEBUG)
logger = logging.getLogger("spamshield")
access_logger = make_http_request_logger()

# Create database tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)
log_current_boot(log_to_console=settings.DEBUG)

app = FastAPI(
    title="SpamShield API",
    version=settings.APP_VERSION,
    description="AI-powered email spam detection system with ML classification, "
                "explainable results, and admin dataset management.",
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


@app.middleware("http")
async def http_access_logger(request: Request, call_next):
    """Log every HTTP request to the access log file."""
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    access_logger.info(
        '%s "%s %s" %s %.1fms client=%s',
        request.method,
        request.url.path,
        request.scope.get("query_string", b"").decode(),
        response.status_code,
        duration_ms,
        request.client.host if request.client else "unknown",
    )
    return response


# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(analysis.router)
app.include_router(history.router)
app.include_router(dashboard.router)
app.include_router(admin.router)
app.include_router(dataset.router)
app.include_router(model.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/", tags=["Root"])
def root():
    return {
        "name": "SpamShield API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "description": "AI-powered email spam detection system",
    }


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "healthy", "version": settings.APP_VERSION}

