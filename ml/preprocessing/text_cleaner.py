"""
Text preprocessing pipeline for email spam detection.
"""
import re
import string
from typing import List, Optional

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    for resource in ["punkt", "stopwords", "wordnet", "punkt_tab", "omw-1.4"]:
        try:
            nltk.data.find(f"tokenizers/{resource}" if resource.startswith("punkt") else f"corpora/{resource}")
        except (LookupError, OSError):
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                # Network / certificate failures must not block import
                pass
except ImportError:
    nltk = None

_STOPWORDS: Optional[set] = None
_LEMMATIZER = None


def _get_stopwords() -> set:
    global _STOPWORDS
    if _STOPWORDS is None and nltk is not None:
        try:
            _STOPWORDS = set(stopwords.words("english"))
        except Exception:
            _STOPWORDS = set()
    else:
        _STOPWORDS = set()
    return _STOPWORDS


def _get_lemmatizer():
    global _LEMMATIZER
    if _LEMMATIZER is None and nltk is not None:
        try:
            _LEMMATIZER = WordNetLemmatizer()
        except Exception:
            _LEMMATIZER = None
    return _LEMMATIZER


def clean_text(text: str, use_lemmatization: bool = False) -> str:
    """Full text cleaning pipeline."""
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http[s]?://\S+|www\.\S+", " url ", text)
    text = re.sub(r"\S+@\S+\.\S+", " email ", text)
    text = re.sub(r"(\+?\d[\d\s\-\(\)]{7,}\d)", " phone ", text)
    text = re.sub(r"\d+", " num ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()

    if nltk is not None:
        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = text.split()
    else:
        tokens = text.split()

    sw = _get_stopwords()
    tokens = [t for t in tokens if t not in sw and len(t) > 1]

    if use_lemmatization:
        lemmatizer = _get_lemmatizer()
        if lemmatizer is not None:
            tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)


def clean_texts(texts: List[str], use_lemmatization: bool = False) -> List[str]:
    """Clean a list of texts."""
    return [clean_text(t, use_lemmatization) for t in texts]
