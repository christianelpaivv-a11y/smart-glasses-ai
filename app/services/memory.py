from typing import List, Dict
import uuid

sessions: Dict[str, List[Dict[str, str]]] = {}
MAX_HISTORY = 10

def get_history(session_id: str) -> List[Dict[str, str]]:
    return sessions.get(session_id, [])[-MAX_HISTORY:]

def get_user_messages(session_id: str) -> List[str]:
    """Return only the content of user messages, in order."""
    history = get_history(session_id)
    return [msg["content"] for msg in history if msg["role"] == "user"]

def get_first_user_message(session_id: str) -> str:
    """Return the first user message, or empty string if none."""
    history = get_history(session_id)
    for msg in history:
        if msg["role"] == "user":
            return msg["content"]
    return ""

def add_message(session_id: str, role: str, content: str):
    if session_id not in sessions:
        sessions[session_id] = []
    sessions[session_id].append({"role": role, "content": content})
    if len(sessions[session_id]) > MAX_HISTORY:
        sessions[session_id] = sessions[session_id][-MAX_HISTORY:]

def create_session() -> str:
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = []
    return session_id
