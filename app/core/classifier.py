def classify_question(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["how", "steps", "process", "recipe", "make", "cook", "build"]):
        return "procedural"
    elif any(w in t for w in ["true or false", "true", "false"]):
        return "true_false"
    elif any(w in t for w in ["multiple choice", "option", "choose"]):
        return "multiple_choice"
    elif any(w in t for w in ["list", "name", "enumerate", "enumeration"]):
        return "enumeration"
    elif any(w in t for w in ["why", "explain", "meaning", "essay", "opinion"]):
        return "essay"
    else:
        return "identification"
