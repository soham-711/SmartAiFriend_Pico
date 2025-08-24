import pvporcupine
import pyaudio
import struct
import time
from config import PORCUPINE_ACCESS_KEY, WAKE_WORD_PATH

class WakeWordDetector:
    def __init__(self):
        try:
            self.porcupine = pvporcupine.create(
                access_key=PORCUPINE_ACCESS_KEY,
                keyword_paths=[WAKE_WORD_PATH]
            )
            self.py_audio = pyaudio.PyAudio()
            self.audio_stream = self.py_audio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
        except Exception as e:
            print(f"Wake detector initialization error: {e}")
            exit(1)

    def detect(self) -> bool:
        print("\n💤 Sleeping... Say 'Hey Pico'", end='', flush=True)
        while True:
            try:
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                if self.porcupine.process(pcm) >= 0:
                    print("\r🎤 Wake word detected!".ljust(50))
                    return True
            except Exception as e:
                print(f"\rWake word error: {e}", end='', flush=True)
                time.sleep(0.1)

    def cleanup(self):
        if hasattr(self, "audio_stream"):
            self.audio_stream.close()
        if hasattr(self, "py_audio"):
            self.py_audio.terminate()
        if hasattr(self, "porcupine"):
            self.porcupine.delete()
