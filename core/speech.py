import speech_recognition as sr
import pyttsx3

class SpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.pause_threshold = 1.0

    def listen(self) -> str:
        for attempt in range(3):  # Try 3 times
            with sr.Microphone() as source:
                print("\n🔴 Listening...", end='', flush=True)
                try:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                    print("\r🟢 Processing...", end='', flush=True)
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"\rYou: {text}")
                    return text
                except sr.UnknownValueError:
                    print("\r🔴 Didn't catch that", end='', flush=True)
                    self.speak("Could you repeat that?")
                except Exception as e:
                    print(f"\rError: {e}", end='', flush=True)
        return ""

    def speak(self, text: str):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Speech error: {e}")
