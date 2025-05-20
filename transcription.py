import whisper

class Transcriber:
    def __init__(self, model_name: str = "small"):
        # Välj modell: tiny, base, small, medium, large
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str) -> str:
        """Transkribera en WAV-fil till text på svenska."""
        result = self.model.transcribe(audio_path, language="sv")
        return result["text"] 