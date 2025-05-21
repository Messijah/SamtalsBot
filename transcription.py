import os
from openai import OpenAI

# Din OpenAI-nyckel måste finns i miljövariabeln OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Transcriber:
    def __init__(self, model="whisper-1"):
        self.model = model

    def transcribe(self, audio_path: str) -> str:
        resp = client.audio.transcriptions.create(
            file=open(audio_path, "rb"),
            model=self.model,
        )
        return resp.text 