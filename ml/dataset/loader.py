"""
Dataset loading and validation for email spam detection.
"""
import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
from ml.utils.config import DATASETS_DIR
from ml.utils.logging_setup import get_ml_logger

logger = get_ml_logger("spamshield.ml.dataset")


def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV dataset and validate its format."""
    path = Path(file_path)
    if not path.exists():
        logger.error("Dataset file not found: %s", file_path)
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    encodings = ["utf-8", "latin-1", "iso-8859-1", "cp1252"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            break
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue

    if df is None:
        logger.error("Could not read CSV file with any supported encoding: %s", file_path)
        raise ValueError(f"Could not read CSV file: {file_path}")

    logger.info("Loaded CSV %s with %d rows and columns %s", file_path, len(df), list(df.columns))
    return df


def validate_dataset(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate that the dataset has the required columns."""
    cols_lower = {c.lower().strip(): c for c in df.columns}

    label_col = None
    text_col = None

    for alias in ["label", "category", "class", "spam"]:
        if alias in cols_lower:
            label_col = cols_lower[alias]
            break

    for alias in ["message", "text", "email", "content", "body", "v2"]:
        if alias in cols_lower:
            text_col = cols_lower[alias]
            break

    if label_col is None:
        logger.warning("Dataset missing label column. Columns: %s", list(df.columns))
        return False, f"Missing label column. Found columns: {list(df.columns)}"
    if text_col is None:
        logger.warning("Dataset missing text column. Columns: %s", list(df.columns))
        return False, f"Missing text column. Found columns: {list(df.columns)}"

    return True, "Valid"


def normalize_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize labels to 'spam' and 'ham'."""
    df = df.copy()
    cols_lower = {c.lower().strip(): c for c in df.columns}

    label_col = None
    for alias in ["label", "category", "class", "spam"]:
        if alias in cols_lower:
            label_col = cols_lower[alias]
            break

    text_col = None
    for alias in ["message", "text", "email", "content", "body", "v2"]:
        if alias in cols_lower:
            text_col = cols_lower[alias]
            break

    if label_col is None or text_col is None:
        raise ValueError("Dataset must have label and text columns")

    label_mapping = {
        "spam": "spam", "ham": "ham",
        "1": "spam", "0": "ham",
        1: "spam", 0: "ham",
        "true": "spam", "false": "ham",
        "yes": "spam", "no": "ham",
    }

    df["label"] = df[label_col].astype(str).str.strip().str.lower().map(label_mapping)
    df["message"] = df[text_col].astype(str)

    df = df[df["label"].isin(["spam", "ham"])].reset_index(drop=True)

    return df[["label", "message"]]


def load_and_prepare(file_path: str) -> Tuple[pd.DataFrame, dict]:
    """Load, validate, and prepare a dataset."""
    df = load_csv(file_path)
    valid, msg = validate_dataset(df)
    if not valid:
        logger.error("Invalid dataset: %s", msg)
        raise ValueError(f"Invalid dataset: {msg}")

    df = normalize_labels(df)

    stats = {
        "total": len(df),
        "spam": int((df["label"] == "spam").sum()),
        "ham": int((df["label"] == "ham").sum()),
        "columns": list(df.columns),
    }
    logger.info("Dataset prepared from %s: total=%d spam=%d ham=%d", file_path, stats["total"], stats["spam"], stats["ham"])

    return df, stats
