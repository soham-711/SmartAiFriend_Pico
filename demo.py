import pyttsx3

engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(i, voice.name, voice.id)

# Choose a voice by index or id
engine.setProperty('voice', voices[1].id)  # example: pick the second voice

# Adjust speech rate (optional)
engine.setProperty('rate', 150)  # default is usually 200

# Speak
engine.say("Hi, I am Pico.")
engine.runAndWait()
