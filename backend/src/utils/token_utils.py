# utils/token_utils.py
import re
from collections import Counter

def tokenize(text: str):
    """
    Splits the input text into lowercase word tokens.
    """
    return re.findall(r'\b\w+\b', text.lower())

def get_search_tokens(product_title: str, word_freq: dict[str, int], threshold: int = 20):
    """
    Returns all tokens from the product title sorted by ascending frequency (rarest first).
    This supports progressive narrowing in search logic. 
    Includes full explanation for tracing/debugging.
    """
    tokens = tokenize(product_title)
    if not tokens:
        return [], {"reason": "no tokens found", "input": product_title}

    # Sort all tokens by their frequency (rarest first)
    sorted_tokens = sorted(tokens, key=lambda t: word_freq.get(t, float("inf")))

    explanation = {
        "original_tokens": tokens,
        "sorted_tokens": sorted_tokens,
        "used_fallback": False,
        "fallback_token": None,
        "fallback_freq": None
    }

    return sorted_tokens, explanation
