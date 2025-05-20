from fastapi import FastAPI, WebSocket
import uvicorn
from transcription import Transcriber
from analysis import ConversationAnalyzer

app = FastAPI()
transcriber = Transcriber()
analyzer = ConversationAnalyzer()

@app.post("/transcribe")
async def transcribe_audio(file_path: str):
    text = transcriber.transcribe(file_path)
    return {"transcript": text}

@app.post("/analyze")
async def analyze_transcript(transcript: str):
    result = analyzer.analyze(transcript)
    return result

@app.websocket("/ws/live")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    buffer = ""
    while True:
        data = await ws.receive_text()
        buffer += data
        if len(buffer.split()) > 50:
            tip = analyzer.analyze(buffer)["analysis"]
            await ws.send_text(tip)
            buffer = ""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 