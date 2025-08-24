import atexit
from core.speech import SpeechEngine
from core.wake_word import WakeWordDetector
from core.conversation import ConversationEngine

class PicoAssistant:
    def __init__(self):
        self.speech = SpeechEngine()
        self.wake = WakeWordDetector()
        self.conversation = ConversationEngine()
        atexit.register(self.cleanup)

    def conversation_loop(self):
        self.speech.speak("Hi friend! I'm Pico. What's on your mind today?")
        while True:
            user_input = self.speech.listen()
            if not user_input:
                continue
            if any(word in user_input for word in ["bye", "goodbye", "exit", "stop"]):
                self.speech.speak("It was great chatting! Just say 'Hey Pico' when you want to talk again.")
                break
            response = self.conversation.generate(user_input)
            print(f"Pico: {response}")
            self.speech.speak(response)

    def run(self):
        print("=== Pico AI Assistant ===")
        print("Initializing... Please wait")
        self.speech.speak("Pico is ready!")
        while True:
            if self.wake.detect():
                self.speech.speak("Yes? I'm listening")
                self.conversation_loop()

    def cleanup(self):
        print("\n🧹 Cleaning up resources...")
        self.wake.cleanup()
