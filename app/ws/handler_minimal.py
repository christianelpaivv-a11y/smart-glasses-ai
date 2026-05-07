from fastapi import WebSocket, WebSocketDisconnect

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("HANDLER MINIMAL CONNECTED")
    try:
        while True:
            data = await websocket.receive_json()
            print("HANDLER MINIMAL ECHO:", data)
            await websocket.send_json({"echo": data})
    except WebSocketDisconnect:
        print("HANDLER MINIMAL DISCONNECTED")
