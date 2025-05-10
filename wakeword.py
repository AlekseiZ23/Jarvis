from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import queue
import os

class WakeWordDetector:
    def __init__(self, model_path="vosk-model-en", wake_phrases=None, device=None):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model not found at: {model_path}")

        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.wake_phrases = [p.lower() for p in (wake_phrases or ["jarvis"])],
        self.q = queue.Queue()
        self.device = device

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio stream status: {status}")
        self.q.put(bytes(indata))

    def wait_for_wake_word(self):
        print("🟢 Waiting for wake word...")

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self._audio_callback,
                               device=self.device):
            while True:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()
                    print("🗣 Recognized:", text)

                    if any(phrase in text for phrase in self.wake_phrases):
                        print("✅ Wake phrase detected!")
                        return

if __name__ == "__main__":
    # Kommentti: Tulostetaan kaikki käytettävissä olevat äänilaitteet
    print("\n🎤 Available audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"ID: {i} - {device['name']}")

    # Kommentti: Aseta oikea mikrofoni-ID
    MIC_DEVICE_ID = 1

    detector = WakeWordDetector(
        wake_phrases=["hey jarvis", "okay jarvis", "jarvis"],
        device=MIC_DEVICE_ID
    )
    detector.wait_for_wake_word()
    print("🔊 Ready to listen for commands...")
