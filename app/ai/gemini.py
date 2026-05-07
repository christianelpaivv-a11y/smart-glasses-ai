import google.generativeai as genai

import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "your-fallback-key"))

def get_ai_response(category: str, text: str, history: list = None, document_text: str = "") -> str:
    # Build conversation context
    context = ""
    if history:
        context = "Previous conversation:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        context += "\n"

    if document_text:
        context += f"Document content:\n{document_text}\n\n"

    # Natural smart assistant prompt – no rigid rules, just intelligence
    prompt = (
        "You are an intelligent, helpful smart glasses assistant. "
        "You can see and understand documents, remember conversations, and answer any question. "
        "Be natural, direct, and concise. "
        "If the question is simple (like a fact, math, multiple choice), give the answer immediately. "
        "If it requires steps (like a recipe or instructions), list them clearly. "
        "Adapt your response to the user's need. Do not add unnecessary commentary or disclaimers.\n\n"
        f"{context}"
        f"User: {text}\n"
        "Assistant:"
    )

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return "I've reached my daily usage limit. Please try again later or switch to a different model."
        else:
            return f"Sorry, something went wrong. ({error_msg[:100]})"
