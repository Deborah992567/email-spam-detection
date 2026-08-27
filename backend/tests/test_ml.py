"""
Tests for the ML module.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def test_text_cleaner():
    from ml.preprocessing.text_cleaner import clean_text

    result = clean_text("Hello WORLD! This is a Test. Visit https://example.com")
    assert "hello" in result.lower()
    assert "url" in result
    assert "https" not in result


def test_text_cleaner_html():
    from ml.preprocessing.text_cleaner import clean_text

    result = clean_text("<p>Hello <b>World</b></p>")
    assert "<p>" not in result
    assert "<b>" not in result
    assert "hello" in result.lower()


def test_text_cleaner_empty():
    from ml.preprocessing.text_cleaner import clean_text
    assert clean_text("") == ""
    assert clean_text(None) == ""


def test_explainer_spam():
    from ml.prediction.explainer import generate_explanation

    text = "FREE WINNER! You won a prize! Click here NOW!!! Act immediately!"
    indicators = generate_explanation(text, "spam", 0.9)
    assert len(indicators) > 0
    types = [i["type"] for i in indicators]
    assert "spam_keywords" in types or "excessive_punctuation" in types


def test_explainer_ham():
    from ml.prediction.explainer import generate_explanation

    text = "Hi, meeting tomorrow at 10am. Let me know if you can make it."
    indicators = generate_explanation(text, "ham", 0.85)
    assert len(indicators) > 0


def test_explainer_urls():
    from ml.prediction.explainer import generate_explanation

    text = "Click https://a.com https://b.com https://c.com https://d.com"
    indicators = generate_explanation(text, "spam", 0.7)
    types = [i["type"] for i in indicators]
    assert "multiple_urls" in types


def test_explainer_sensitive():
    from ml.prediction.explainer import generate_explanation

    text = "Please send your credit card number and password to verify your account"
    indicators = generate_explanation(text, "spam", 0.9)
    types = [i["type"] for i in indicators]
    assert "sensitive_info_request" in types


def test_dataset_loader_validation():
    import pandas as pd
    from ml.dataset.loader import validate_dataset

    df_valid = pd.DataFrame({"label": ["spam", "ham"], "message": ["test1", "test2"]})
    valid, msg = validate_dataset(df_valid)
    assert valid

    df_invalid = pd.DataFrame({"col1": ["a"], "col2": ["b"]})
    valid, msg = validate_dataset(df_invalid)
    assert not valid


def test_dataset_normalize():
    import pandas as pd
    from ml.dataset.loader import normalize_labels

    df = pd.DataFrame({"label": ["spam", "ham", "1", "0"], "message": ["a", "b", "c", "d"]})
    result = normalize_labels(df)
    assert list(result["label"]) == ["spam", "ham", "spam", "ham"]


def test_model_manager_registry(tmp_path):
    from ml.utils import config
    import json
    original = config.MODELS_DIR
    config.MODELS_DIR = tmp_path
    config.MODEL_REGISTRY_PATH = tmp_path / "registry.json"

    from ml.models.model_manager import _load_registry, _save_registry
    registry = _load_registry()
    assert registry == []

    _save_registry([{"version": "v1"}])
    registry = _load_registry()
    assert len(registry) == 1

    config.MODELS_DIR = original
