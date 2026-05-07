from fastapi import WebSocket, WebSocketDisconnect
from ..core.router import process_question
from ..services.tts import stream_tts_chunks
from ..services.memory import (
    get_history, add_message, create_session,
    get_user_messages, get_first_user_message
)

META_QUESTIONS = {
    "what was my first question": "first_question",
    "what was my last question": "last_question",
    "what did i ask before": "last_question",
    "repeat my last question": "last_question",
    "list my questions": "all_questions",
    "what have i asked so far": "all_questions",
    "what were my questions": "all_questions",
    "how many questions have i asked": "count_questions",
}

def handle_meta_question(text: str, session_id: str) -> str:
    normalized = text.strip().lower()
    intent = None
    for pattern, action in META_QUESTIONS.items():
        if pattern in normalized:
            intent = action
            break
    if intent is None:
        return None
    if intent == "first_question":
        first = get_first_user_message(session_id)
        return f"Your first question was: \"{first}\"." if first else "You haven't asked any questions yet."
    if intent == "last_question":
        user_msgs = get_user_messages(session_id)
        return f"Your last question was: \"{user_msgs[-1]}\"." if user_msgs else "You haven't asked any questions yet."
    if intent == "all_questions":
        user_msgs = get_user_messages(session_id)
        if not user_msgs:
            return "You haven't asked any questions yet."
        numbered = [f"{i+1}. {q}" for i, q in enumerate(user_msgs)]
        return "Here are the questions you've asked:\n" + "\n".join(numbered)
    if intent == "count_questions":
        count = len(get_user_messages(session_id))
        return f"You have asked {count} question{'s' if count != 1 else ''} so far."
    return None


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🚀 STREAMING HANDLER CONNECTED")
    session_id = None
    try:
        while True:
            data = await websocket.receive_json()
            print("📥 RECEIVED:", data)
            if "session_id" in data:
                session_id = data["session_id"]
            else:
                session_id = create_session()
                await websocket.send_json({"session_id": session_id})
                if not data.get("text"):
                    continue

            text = data.get("text", "")
            motion = data.get("motion", False)
            document = data.get("document", False)
            document_text = data.get("document_text", "")

            if motion and document:
                add_message(session_id, "user", text)

                meta_answer = handle_meta_question(text, session_id)
                if meta_answer is not None:
                    answer = meta_answer
                    category = "meta"
                    add_message(session_id, "assistant", answer)
                    # Send step start
                    await websocket.send_json({
                        "step_start": {
                            "type": category,
                            "step": 1,
                            "total_steps": 1,
                            "text": answer
                        }
                    })
                    # Stream audio chunks
                    async for chunk in stream_tts_chunks(answer):
                        await websocket.send_json({"audio_chunk": chunk})
                    await websocket.send_json({"step_end": True})
                else:
                    try:
                        history = get_history(session_id)
                        result = process_question(text, history=history, document_text=document_text)
                        answer = result["answer"]
                        category = result["category"]
                    except Exception as ai_err:
                        answer = f"I'm sorry, something went wrong. ({str(ai_err)[:100]})"
                        category = "error"

                    add_message(session_id, "assistant", answer)

                    # Split into steps (or whole answer)
                    steps = [
                        line.strip()
                        for line in answer.split("\n")
                        if line.strip() and line.strip()[0].isdigit()
                    ]
                    if not steps:
                        steps = [answer]

                    for idx, step in enumerate(steps, 1):
                        await websocket.send_json({
                            "step_start": {
                                "type": category,
                                "step": idx,
                                "total_steps": len(steps),
                                "text": step.strip()
                            }
                        })
                        async for chunk in stream_tts_chunks(step.strip()):
                            await websocket.send_json({"audio_chunk": chunk})
                        await websocket.send_json({"step_end": True})
            else:
                await websocket.send_json({
                    "info": "Trigger not met",
                    "motion": motion,
                    "document": document
                })
    except WebSocketDisconnect:
        print("🔌 CLIENT DISCONNECTED")
