"""
Model evaluation utilities.
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from typing import Dict, Optional
from ml.utils.logging_setup import get_ml_logger

logger = get_ml_logger("spamshield.ml.evaluation")


def evaluate_model(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
) -> Dict[str, float]:
    """Evaluate model predictions and return metrics."""
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    cm = confusion_matrix(y_true, y_pred).tolist()
    logger.info("Evaluated model -> accuracy=%.4f precision=%.4f recall=%.4f f1=%.4f", acc, prec, rec, f1)

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "confusion_matrix": cm,
        "classification_report": classification_report(
            y_true, y_pred, target_names=["ham", "spam"], zero_division=0
        ),
    }
