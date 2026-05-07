from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from app.ws.handler import websocket_endpoint

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "alive"}

@app.get("/smart_glasses.html")
async def get_glasses_page():
    return FileResponse("smart_glasses.html")

@app.get("/mobile.html")
async def get_mobile_page():
    return FileResponse("mobile.html")

@app.get("/ws_test.html")
async def get_ws_test():
    return FileResponse("ws_test.html")

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("manifest.json")

@app.get("/sw.js")
async def get_service_worker():
    return FileResponse("sw.js")

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket_endpoint(websocket)
