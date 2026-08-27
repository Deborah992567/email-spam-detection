"""
ML Module Configuration.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "ml"
MODELS_DIR = ML_DIR / "models"
DATASETS_DIR = ML_DIR / "dataset"
SAVED_MODELS_DIR = MODELS_DIR / "saved"

for d in [MODELS_DIR, DATASETS_DIR, SAVED_MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

MODEL_REGISTRY_PATH = MODELS_DIR / "model_registry.json"

TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_MIN_DF = 2
TFIDF_MAX_DF = 0.95
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_EMAIL_LENGTH = 50000
