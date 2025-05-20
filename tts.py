from gtts import gTTS
import os

def speak(text: str, filename: str = "output.mp3"):
    tts = gTTS(text=text, lang='sv')
    tts.save(filename)
    os.system(f"ffplay -nodisp -autoexit {filename} > /dev/null 2>&1") 