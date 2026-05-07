"""
Simple in-memory cache for Q&A pairs.
"""
import re

# cache_data: normalized question -> {"answer": ..., "category": ...}
cache_data = {}
MAX_CACHE_SIZE = 200

def _normalize(text: str) -> str:
    """Normalize question text for cache key."""
    return re.sub(r'\s+', ' ', text.lower().strip())

def get_cached_response(question: str) -> dict:
    """Return cached {answer, category} or None."""
    key = _normalize(question)
    return cache_data.get(key)

def add_to_cache(question: str, category: str, answer: str):
    """Store an answer in cache."""
    key = _normalize(question)
    if len(cache_data) >= MAX_CACHE_SIZE:
        # remove oldest entry (first key)
        oldest = next(iter(cache_data))
        del cache_data[oldest]
    cache_data[key] = {"category": category, "answer": answer}
