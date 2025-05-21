from openai import OpenAI
import os

# Din OpenAI-nyckel måste finns i miljövariabeln OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Transcriber:
    def __init__(self):
        pass

    def transcribe(self, audio_path: str) -> str:
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                file=f,
                model="whisper-1",
                response_format="text",
            )
        return transcript 