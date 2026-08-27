"""
Explainable spam detection indicators.
"""
import re
from typing import List, Dict

SPAM_KEYWORDS = [
    "free", "winner", "congratulations", "prize", "claim", "click here",
    "act now", "limited time", "urgent", "offer", "deal", "discount",
    "buy now", "order now", "subscribe", "unsubscribe", "credit card",
    "loan", "mortgage", "viagra", "cialis", "enhancement", "pharmacy",
    "nigerian", "inheritance", "million dollars", "wire transfer",
    "verify your account", "confirm your identity", "suspended",
    "account alert", "security alert", "unauthorized", "immediately",
    "no cost", "no obligation", "risk free", "guarantee", "amazing",
    "incredible", "fantastic", "once in a lifetime", "you have been selected",
    "call now", "operators are standing by", "double your", "triple your",
    "earn money", "work from home", "extra income", "financial freedom",
]

SENSITIVE_KEYWORDS = [
    "password", "credit card", "social security", "bank account",
    "routing number", "pin number", "ssn", "passport", "driver license",
    "login credentials", "verify your", "confirm your",
]

URGENCY_KEYWORDS = [
    "act now", "limited time", "expires", "hurry", "don't delay",
    "before it's too late", "last chance", "final notice", "deadline",
    "urgent", "immediate", "asap", "right away", "only today",
    "today only", "running out", "almost gone",
]

PROMO_KEYWORDS = [
    "free", "offer", "deal", "discount", "save", "sale",
    "bargain", "cheap", "lowest price", "best price", "special offer",
    "exclusive deal", "limited offer", "bonus", "reward",
]


def generate_explanation(text: str, prediction: str, confidence: float) -> List[Dict[str, str]]:
    """Generate human-readable indicators for the prediction."""
    indicators = []
    text_lower = text.lower()

    total_chars = len(text)
    upper_chars = sum(1 for c in text if c.isupper())
    if total_chars > 10 and (upper_chars / total_chars) > 0.3:
        indicators.append({
            "type": "excessive_caps",
            "severity": "medium",
            "description": f"Excessive use of capital letters ({round(upper_chars/total_chars*100, 1)}% of text is uppercase).",
        })

    urls = re.findall(r'https?://\S+|www\.\S+', text)
    if len(urls) >= 3:
        indicators.append({
            "type": "multiple_urls",
            "severity": "high",
            "description": f"Contains {len(urls)} URLs/links, which is common in spam emails.",
        })
    elif len(urls) >= 1:
        indicators.append({
            "type": "has_urls",
            "severity": "low",
            "description": "Email contains URLs.",
        })

    exclamation_count = text.count("!")
    if exclamation_count >= 3:
        indicators.append({
            "type": "excessive_punctuation",
            "severity": "medium",
            "description": f"Excessive use of exclamation marks ({exclamation_count} found).",
        })

    found_spam = [kw for kw in SPAM_KEYWORDS if kw in text_lower]
    if len(found_spam) >= 3:
        indicators.append({
            "type": "spam_keywords",
            "severity": "high",
            "description": f"Contains multiple spam-related keywords: {', '.join(found_spam[:5])}.",
        })
    elif found_spam:
        indicators.append({
            "type": "spam_keywords",
            "severity": "low",
            "description": f"Contains potential spam keywords: {', '.join(found_spam[:3])}.",
        })

    found_sensitive = [kw for kw in SENSITIVE_KEYWORDS if kw in text_lower]
    if found_sensitive:
        indicators.append({
            "type": "sensitive_info_request",
            "severity": "high",
            "description": f"Requests sensitive information: {', '.join(found_sensitive)}.",
        })

    found_urgency = [kw for kw in URGENCY_KEYWORDS if kw in text_lower]
    if len(found_urgency) >= 2:
        indicators.append({
            "type": "urgency_language",
            "severity": "high",
            "description": f"Uses urgency language: {', '.join(found_urgency[:3])}.",
        })
    elif found_urgency:
        indicators.append({
            "type": "urgency_language",
            "severity": "low",
            "description": f"Contains urgency wording: {', '.join(found_urgency)}.",
        })

    found_promo = [kw for kw in PROMO_KEYWORDS if kw in text_lower]
    if len(found_promo) >= 3:
        indicators.append({
            "type": "promotional_language",
            "severity": "medium",
            "description": f"Uses promotional language: {', '.join(found_promo[:4])}.",
        })

    no_reply = re.search(r"no[\s\-]?reply|do[\s\-]?not[\s\-]?reply", text_lower)
    if no_reply:
        indicators.append({
            "type": "suspicious_sender",
            "severity": "low",
            "description": "Sent from a no-reply or automated address pattern.",
        })

    dollar_amounts = re.findall(r'\$[\d,]+\.?\d*', text)
    if dollar_amounts:
        indicators.append({
            "type": "monetary_amounts",
            "severity": "medium",
            "description": f"References specific monetary amounts: {', '.join(dollar_amounts[:3])}.",
        })

    if not indicators:
        if prediction == "spam":
            indicators.append({
                "type": "model_prediction",
                "severity": "low",
                "description": "The overall text pattern was flagged by the ML model based on learned patterns.",
            })
        else:
            indicators.append({
                "type": "clean",
                "severity": "none",
                "description": "No significant spam indicators detected. The email appears to be legitimate.",
            })

    return indicators
