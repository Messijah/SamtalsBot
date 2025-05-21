import openai
import os

# Din OpenAI-nyckel måste finns i miljövariabeln OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

class Transcriber:
    def __init__(self, model="whisper-1"):
        self.model = model

    def transcribe(self, audio_path: str) -> str:
        with open(audio_path, "rb") as f:
            result = openai.Audio.transcribe(
                model=self.model,
                file=f,
                response_format="text"
            )
        # Whisper API ger tillbaka en sträng i response_format="text"
        if isinstance(result, str):
            return result
        # fallback om du mot förmodan byter format till JSON
        return result.get("text", "") 