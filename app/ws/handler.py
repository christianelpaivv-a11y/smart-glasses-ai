from fastapi import WebSocket, WebSocketDisconnect
from ..core.router import process_question
from ..services.tts import text_to_speech_base64   # <-- non-streaming function
from ..services.memory import (
    get_history, add_message, create_session,
    get_user_messages, get_first_user_message
)

META_QUESTIONS = {
    "what was my first question": "first_question",
    "what was my last question": "last_question",
    # ... keep all the meta-questions exactly as before ...
}

def handle_meta_question(text: str, session_id: str) -> str:
    # ... keep the exact same meta-question handling ...
    return None

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # ... 
    # Inside the motion/document check, use text_to_speech_base64 for each step
    for idx, step in enumerate(steps, 1):
        audio_b64 = await text_to_speech_base64(step.strip())
        await websocket.send_json({
            "type": category,
            "step": idx,
            "total_steps": len(steps),
            "text": step.strip(),
            "audio_base64": audio_b64
        })