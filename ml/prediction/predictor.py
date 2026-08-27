"""
Prediction engine for email spam detection.
"""
from typing import Dict, Any, Optional, Tuple
from ml.models.model_manager import load_latest_model, get_latest_version
from ml.preprocessing.text_cleaner import clean_text
from ml.prediction.explainer import generate_explanation
import numpy as np


def predict_email(
    sender: str,
    subject: str,
    body: str,
    model=None,
    vectorizer=None,
) -> Dict[str, Any]:
    """Predict if an email is spam or ham."""
    if model is None or vectorizer is None:
        model, vectorizer, version_info = load_latest_model()
    else:
        version_info = get_latest_version() or {"version": "unknown", "algorithm": "unknown"}

    combined_text = f"{subject} {body}"
    cleaned = clean_text(combined_text)

    features = vectorizer.transform([cleaned])

    prediction = model.predict(features)[0]

    confidence = 0.5
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        confidence = float(proba[int(prediction)])
    elif hasattr(model, "decision_function"):
        decision = model.decision_function(features)[0]
        confidence = float(1 / (1 + np.exp(-decision)))

    label = "spam" if prediction == 1 else "ham"

    if confidence >= 0.8:
        risk_level = "high"
    elif confidence >= 0.5:
        risk_level = "medium"
    else:
        risk_level = "low"

    raw_text = f"{subject} {body}"
    indicators = generate_explanation(raw_text, label, confidence)

    return {
        "prediction": label,
        "confidence": round(confidence * 100, 1),
        "risk_level": risk_level,
        "indicators": indicators,
        "model_version": version_info.get("version", "unknown"),
        "algorithm": version_info.get("algorithm", "unknown"),
    }
