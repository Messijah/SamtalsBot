from audio_capture import AudioRecorder
from transcription import Transcriber
from analysis import ConversationAnalyzer

if __name__ == "__main__":
    print("SamtalsBot - Test")
    print("-----------------")
    print("Spelar in 10 sekunder ljud...")
    
    # 1) Spela in (10 sekunder)
    recorder = AudioRecorder()
    thread = recorder.start_recording(filename="session.wav", duration=10)
    thread.join()

    print("\nTranskriberar ljudet...")
    # 2) Transkribera
    transcriber = Transcriber(model_name="small")
    transcript = transcriber.transcribe("session.wav")
    print("\n--- Transkript ---")
    print(transcript, "\n")

    print("Analyserar samtalet...")
    # 3) Analysera
    analyzer = ConversationAnalyzer()
    analysis = analyzer.analyze(transcript)
    print("\n--- Analys ---")
    print(analysis["analysis"]) 