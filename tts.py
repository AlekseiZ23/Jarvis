import pygame
import os
import random
from pathlib import Path
import pyttsx3  # Kommentti: Käytetään TTS:ää (pyttsx3)

# Kommentti: Polku kansioon, jossa on valmiita äänitiedostoja
AUDIO_DIR = Path(__file__).parent / "audio"

# Kommentti: Alustetaan pyttsx3 puhesynteesille
engine = pyttsx3.init()

# Kommentti: Audion toistamisen funktio
def play_audio(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(str(file_path))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Audio playback error: {e}")

# Kommentti: Pääfunktio puheen toistoon
def speak(text):
    predefined = {
        "ok": ["ok1.wav", "ok2.wav"],
        "not found": ["not_found.wav"]
    }

    # Kommentti: Tarkistetaan, sisältääkö teksti valmiita fraaseja
    for key, files in predefined.items():
        if key in text.lower():
            audio_file = AUDIO_DIR / random.choice(files)
            if audio_file.exists():
                print("Jarvis (audio):", audio_file.name)
                play_audio(audio_file)
                return

    # Kommentti: Muussa tapauksessa käytetään synteesiä
    print("Jarvis (TTS):", text)
    engine.say(text)  
    engine.runAndWait()

# Kommentti: Esimerkkikäyttö
if __name__ == "__main__":
    speak("Hello, how can I help you?")