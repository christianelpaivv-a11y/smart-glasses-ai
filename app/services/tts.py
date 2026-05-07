import edge_tts
import base64

VOICE = "en-US-AriaNeural"

async def text_to_speech_base64(text: str) -> str:
    """Keep for backward compatibility – not used by streaming handler."""
    import tempfile, os
    communicate = edge_tts.Communicate(text, VOICE)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = tmp.name
    await communicate.save(tmp_path)
    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()
    os.unlink(tmp_path)
    return base64.b64encode(audio_bytes).decode("utf-8")

async def stream_tts_chunks(text: str):
    """
    Async generator that yields base64-encoded MP3 chunks.
    """
    communicate = edge_tts.Communicate(text, VOICE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield base64.b64encode(chunk["data"]).decode("utf-8")
