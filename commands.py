import os
import pygame
import openai
from tts import speak
from dotenv import load_dotenv
import pyttsx3
import subprocess
import ctypes
import webbrowser
import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key:
    print("API key loaded successfully!")
else:
    print("Failed to load API key.")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "David" in voice.name:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an English-speaking voice assistant. Respond only in English."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"❌ Error while calling ChatGPT: {e}")
        return "Sorry, I couldn't get a response."

def interpret(text):
    text = text.lower()

    if "hello" in text:
        return {"action": "greet"}
    elif "what can you do" in text or "your capabilities" in text:
        return {"action": "capabilities"}
    elif "tell me a joke" in text or "joke" in text:
        return {"action": "joke"}
    elif "open browser" in text or "launch chrome" in text:
        return {"action": "open_browser"}
    elif "close chrome" in text:
        return {"action": "close_browser"}
    elif "open youtube" in text:
        return {"action": "open_youtube"}
    elif "volume up" in text:
        return {"action": "volume_up"}
    elif "volume down" in text:
        return {"action": "volume_down"}
    elif "mute" in text:
        return {"action": "mute"}
    elif "open notepad" in text:
        return {"action": "open_notepad"}
    elif "open calculator" in text:
        return {"action": "open_calculator"}
    elif "search for" in text:
        query = text.split("search for", 1)[-1].strip()
        return {"action": "google_search", "query": query}
    elif "shutdown computer" in text:
        return {"action": "shutdown"}
    elif "what time is it" in text:
        return {"action": "get_time"}
    elif "what's the date" in text or "what is the date" in text:
        return {"action": "get_date"}
    elif "weather" in text:
        return {"action": "get_weather", "city": "London"}
    elif any(word in text for word in ["bye", "goodbye", "shutdown"]):
        return {"action": "bye"}
    else:
        return {"action": "ask_anything"}

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    pygame.mixer.music.wait()

def set_volume(level):
    devices = ctypes.windll.user32
    volume = int(level * 65535 / 100)
    ctypes.windll.user32.SendMessageW(0xffff, 0x319, 0, (0xA0000 | (volume << 16)))

def execute_command(intent_data, text=None):
    if not intent_data:
        speak("I didn't understand the command.")
        return

    action = intent_data.get("action")

    if action == "greet":
        speak("Hello! How can I help you?")
    elif action == "capabilities":
        speak("I can open a browser, answer questions, control volume, search the web, and more.")
    elif action == "joke":
        play_audio("audio/joke2.wav")
    elif action == "open_browser":
        try:
            os.system("start chrome")
            speak("Opening browser.")
        except Exception as e:
            speak("Failed to open browser.")
            print(f"Error while opening browser: {e}")
    elif action == "close_browser":
        os.system("taskkill /im chrome.exe /f")
        speak("Closing Chrome.")
    elif action == "open_youtube":
        os.system("start https://www.youtube.com")
        speak("Opening YouTube.")
    elif action == "volume_up":
        os.system("nircmd.exe changesysvolume 5000")
        speak("Turning volume up.")
    elif action == "volume_down":
        os.system("nircmd.exe changesysvolume -5000")
        speak("Turning volume down.")
    elif action == "mute":
        os.system("nircmd.exe mutesysvolume 1")
        speak("Volume muted.")
    elif action == "open_notepad":
        os.system("start notepad")
        speak("Opening Notepad.")
    elif action == "open_calculator":
        os.system("start calc")
        speak("Opening Calculator.")
    elif action == "google_search":
        query = intent_data.get("query", "")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching Google for {query}.")
    elif action == "shutdown":
        speak("Shutting down the computer.")
        os.system("shutdown /s /t 5")
    elif action == "get_time":
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}.")
    elif action == "get_date":
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}.")
    elif action == "get_weather":
        city = intent_data.get("city", "unknown city")
        speak(f"The weather in {city} is sunny and 20 degrees.")
    elif action == "ask_anything" and text:
        response = ask_gpt(text)
        speak(response)
    elif action == "bye":
        speak("Goodbye!")
    else:
        speak("I didn't understand the command.")
        print(f"Unknown command: {action}")