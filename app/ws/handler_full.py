from fastapi import WebSocket, WebSocketDisconnect
from ..core.router import process_question
from ..services.tts import text_to_speech_base64

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    try:
        while True:
            data = await websocket.receive_json()
            print("RECEIVED:", data)
            text = data.get("text", "")
            motion = data.get("motion", False)
            document = data.get("document", False)

            if motion and document:
                result = process_question(text)
                answer = result["answer"]
                category = result["category"]

                # Split into steps (lines starting with a digit)
                steps = [
                    line.strip()
                    for line in answer.split("\n")
                    if line.strip() and line.strip()[0].isdigit()
                ]
                if not steps:
                    steps = [answer]

                for idx, step in enumerate(steps, 1):
                    audio_b64 = await text_to_speech_base64(step.strip())
                    await websocket.send_json({
                        "type": category,
                        "step": idx,
                        "total_steps": len(steps),
                        "text": step.strip(),
                        "audio_base64": audio_b64
                    })
            else:
                await websocket.send_json({
                    "info": "Trigger not met",
                    "motion": motion,
                    "document": document
                })
    except WebSocketDisconnect:
        print("Client disconnected")
