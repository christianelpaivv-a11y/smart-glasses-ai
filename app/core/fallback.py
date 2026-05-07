"""
Predefined answers for common questions.
"""

FALLBACK_ANSWERS = {
    "what is your name": "I'm your Smart Glasses assistant.",
    "who are you": "I'm an AI assistant running on these glasses.",
    "what can you do": "I can answer questions, give step-by-step instructions, and remember our conversation.",
    "hello": "Hi there! How can I help?",
    "hi": "Hello!",
    "good morning": "Good morning! Ready to assist.",
    "good afternoon": "Good afternoon! How can I help?",
    "good evening": "Good evening!",
    "what is the capital of france": "The capital of France is Paris.",
    "what is 2+2": "2 + 2 equals 4.",
    "what is the meaning of life": "That's a deep question! Many people say 42, but I think it's about being helpful.",
    "tell me a joke": "Why did the smart glasses break up with the smartphone? Because it found a better connection!",
    "what is the population of tokyo": "The population of Tokyo is approximately 14 million in the city proper.",
    "translate hello to spanish": "Hola",
    "how do i restart my router": "1. Unplug the router.\n2. Wait 10 seconds.\n3. Plug it back in.\n4. Wait 2 minutes for it to reconnect.",
}

def get_fallback_response(question: str, category: str) -> str:
    """
    Return a predefined answer for the exact question (normalized), or None.
    """
    normalized = question.lower().strip()
    return FALLBACK_ANSWERS.get(normalized)
