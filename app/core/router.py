from .classifier import classify_question
from ..ai.gemini import get_ai_response
from .cache import get_cached_response, add_to_cache
from .fallback import get_fallback_response
from typing import List, Dict, Optional

def process_question(text: str, history: Optional[List[Dict[str, str]]] = None, document_text: str = "") -> dict:
    # Always classify the question first
    category = classify_question(text)

    # 1. Check cache
    cached = get_cached_response(text)
    if cached:
        print(f"CACHE HIT for: {text}")
        return cached

    # 2. Check fallback dictionary
    fallback_answer = get_fallback_response(text, category)
    if fallback_answer:
        print(f"FALLBACK used for: {text}")
        add_to_cache(text, category, fallback_answer)
        return {"category": category, "answer": fallback_answer}

    # 3. Try AI
    try:
        answer = get_ai_response(category, text, history=history, document_text=document_text)
        print(f"AI responded for: {text}")
        add_to_cache(text, category, answer)
        return {"category": category, "answer": answer}
    except Exception as e:
        print(f"AI call failed for: {text} → {e}")
        generic_answer = "I'm sorry, I can't answer that right now. Please try again later."
        return {"category": category, "answer": generic_answer}
