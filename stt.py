from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import os

# Kommentti: Mallin polku — muokkaa tarvittaessa
MODEL_PATH = "vosk-model-ru"

# Kommentti: Globaali jono äänen datalle
q = queue.Queue()

# Kommentti: Kuuntelee puhetta aktivoinnin jälkeen (yhden lauseen), palauttaa tekstin
def listen_for_speech():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Vosk model not found at: {MODEL_PATH}")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    def callback(indata, frames, time, status):
        if status:
            print(f"Audio status: {status}")
        q.put(bytes(indata))

    print("🎙 Waiting for voice command...")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                print(f"✅ Recognized: {text}")
                return text
