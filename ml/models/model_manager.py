"""
Model versioning and persistence.
"""
import json
import joblib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any
from ml.utils import config
from ml.utils.logging_setup import get_ml_logger

logger = get_ml_logger("spamshield.ml.models")


def _load_registry() -> list:
    if config.MODEL_REGISTRY_PATH.exists():
        with open(config.MODEL_REGISTRY_PATH, "r") as f:
            return json.load(f)
    return []


def _save_registry(registry: list):
    with open(config.MODEL_REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def save_model_version(
    algorithm: str,
    model: Any,
    vectorizer: Any,
    metrics: Dict[str, float],
) -> str:
    """Save a model version and return its ID."""
    registry = _load_registry()
    version_num = len(registry) + 1
    version_id = f"v{version_num}"
    model_path = config.SAVED_MODELS_DIR / f"model_{version_id}.joblib"
    vec_path = config.SAVED_MODELS_DIR / f"vectorizer_{version_id}.joblib"

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)

    entry = {
        "id": version_num,
        "version": version_id,
        "algorithm": algorithm,
        "accuracy": round(float(metrics.get("accuracy", 0)), 4),
        "precision": round(float(metrics.get("precision", 0)), 4),
        "recall": round(float(metrics.get("recall", 0)), 4),
        "f1_score": round(float(metrics.get("f1_score", 0)), 4),
        "model_path": str(model_path),
        "vectorizer_path": str(vec_path),
        "trained_at": datetime.now(timezone.utc).isoformat(),
    }

    registry.append(entry)
    _save_registry(registry)

    # Update latest symlink reference
    latest_path = config.SAVED_MODELS_DIR / "latest.json"
    with open(latest_path, "w") as f:
        json.dump(entry, f, indent=2)

    logger.info("Saved model version %s (algorithm=%s, f1=%.4f)", version_id, algorithm, metrics.get("f1_score", 0))
    return version_id


def get_latest_version() -> Optional[Dict[str, Any]]:
    """Get the latest model version info."""
    latest_path = config.SAVED_MODELS_DIR / "latest.json"
    if latest_path.exists():
        with open(latest_path, "r") as f:
            return json.load(f)
    registry = _load_registry()
    if registry:
        return registry[-1]
    return None


def load_latest_model():
    """Load the latest model and vectorizer."""
    info = get_latest_version()
    if info is None:
        logger.warning("Attempted to load model but no trained model exists")
        raise FileNotFoundError("No trained model found. Please train a model first.")
    model = joblib.load(info["model_path"])
    vectorizer = joblib.load(info["vectorizer_path"])
    logger.info("Loaded model %s (%s) from disk", info.get("version"), info.get("algorithm"))
    return model, vectorizer, info


def get_registry() -> list:
    """Get the full model registry."""
    return _load_registry()
