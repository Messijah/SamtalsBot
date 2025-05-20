import sounddevice as sd
import numpy as np
import queue
import threading
from scipy.io.wavfile import write

class AudioRecorder:
    def __init__(self, samplerate=16000, channels=1, chunk=1024):
        self.samplerate = samplerate
        self.channels = channels
        self.chunk = chunk
        self.q = queue.Queue()
        self.recording = False

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"Inspelning status: {status}")
        self.q.put(indata.copy())

    def start_recording(self, filename: str = "recording.wav", duration: int = None) -> threading.Thread:
        """
        Starta inspelning. Stannar efter `duration` sekunder om angett, annars tills stop_recording().
        """
        self.recording = True
        frames = []
        stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            blocksize=self.chunk,
            callback=self._callback
        )
        stream.start()

        def _record():
            import time
            start = time.time()
            while self.recording:
                data = self.q.get()
                frames.append(data)
                if duration and (time.time() - start) > duration:
                    break
            stream.stop()
            audio = np.concatenate(frames, axis=0)
            write(filename, self.samplerate, audio)
            print(f"Inspelning sparad som {filename}")

        thread = threading.Thread(target=_record)
        thread.start()
        return thread

    def stop_recording(self):
        self.recording = False 