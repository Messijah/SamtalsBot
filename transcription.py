import os
import openai

# Din OpenAI-nyckel måste finns i miljövariabeln OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

class Transcriber:
    def __init__(self, model: str = "whisper-1"):
        self.model = model

    def transcribe(self, audio_path: str) -> str:
        with open(audio_path, "rb") as audio_file:
            result = openai.Audio.transcribe(
                model=self.model,
                file=audio_file,
                response_format="text"
            )
        return result 