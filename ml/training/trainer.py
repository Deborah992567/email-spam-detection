"""
Model training pipeline for email spam detection.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from typing import Dict, Any, Tuple
from ml.preprocessing.text_cleaner import clean_texts
from ml.evaluation.evaluator import evaluate_model
from ml.models.model_manager import save_model_version
from ml.utils.config import (
    TFIDF_MAX_FEATURES, TFIDF_NGRAM_RANGE, TFIDF_MIN_DF,
    TFIDF_MAX_DF, TEST_SIZE, RANDOM_STATE
)
from ml.utils.logging_setup import get_ml_logger

logger = get_ml_logger()


def train_models(df: pd.DataFrame) -> Dict[str, Any]:
    """Train multiple models and return results."""
    if df.empty:
        logger.error("Training attempted with an empty dataset")
        raise ValueError("Training dataset is empty")

    texts = df["message"].tolist()
    labels = df["label"].map({"spam": 1, "ham": 0}).values

    if len(set(labels)) < 2:
        logger.error("Training dataset must contain both spam and ham samples")
        raise ValueError("Training dataset must contain both spam and ham samples")

    n_spam = int(labels.sum())
    n_ham = int(len(labels) - n_spam)
    logger.info("Starting training with %d samples (spam=%d, ham=%d)", len(df), n_spam, n_ham)

    cleaned = clean_texts(texts)

    X_train, X_test, y_train, y_test = train_test_split(
        cleaned, labels, test_size=TEST_SIZE,
        random_state=RANDOM_STATE, stratify=labels,
    )

    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        min_df=TFIDF_MIN_DF,
        max_df=TFIDF_MAX_DF,
        sublinear_tf=True,
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    logger.info("TF-IDF vectorization complete (train=%d, test=%d)", X_train_vec.shape[0], X_test_vec.shape[0])

    models = {
        "MultinomialNB": MultinomialNB(alpha=1.0),
        "LogisticRegression": LogisticRegression(
            max_iter=1000, random_state=RANDOM_STATE, C=1.0
        ),
        "LinearSVC": CalibratedClassifierCV(
            LinearSVC(max_iter=2000, random_state=RANDOM_STATE), cv=3
        ),
    }

    results = {}
    best_f1 = -1
    best_name = None

    for name, model in models.items():
        model.fit(X_train_vec, y_train)
        y_pred = model.predict(X_test_vec)
        y_proba = None
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test_vec)[:, 1]

        metrics = evaluate_model(y_test, y_pred, y_proba)
        results[name] = metrics
        metrics["model"] = model
        logger.info(
            "Model %s -> accuracy=%.4f precision=%.4f recall=%.4f f1=%.4f",
            name, metrics["accuracy"], metrics["precision"], metrics["recall"], metrics["f1_score"],
        )

        if metrics["f1_score"] > best_f1:
            best_f1 = metrics["f1_score"]
            best_name = name

    best_metrics = results[best_name]
    best_model = best_metrics.pop("model")

    version_id = save_model_version(
        algorithm=best_name,
        model=best_model,
        vectorizer=vectorizer,
        metrics=best_metrics,
    )
    logger.info("Best model '%s' saved as version %s (F1=%.4f)", best_name, version_id, best_f1)

    return {
        "best_model": best_name,
        "best_version": version_id,
        "results": {
            name: {k: v for k, v in m.items() if k != "model"}
            for name, m in results.items()
        },
        "train_size": len(X_train),
        "test_size": len(X_test),
        "total_samples": len(df),
    }
