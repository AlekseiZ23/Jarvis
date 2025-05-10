import tkinter as tk
import threading
from tkinter import scrolledtext
import traceback
from commands import execute_command, interpret, speak
import speech_recognition as sr
from PIL import Image, ImageTk, ImageSequence

# Kommentti: Puheen tunnistuksen funktio
def listen_for_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='en-US')
            return text
        except sr.UnknownValueError:
            print("Could not recognize speech.")
            return None
        except sr.RequestError:
            print("Error connecting to the speech recognition service.")
            return None

# Kommentti: GUI:n luonti
class JarvisGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("JARVIS AI Assistant")
        self.master.geometry("720x560")
        self.master.configure(bg="#0f0f0f")

        # Kommentti: Animoidun taustan lataus ja valmistelu
        self.bg_label = tk.Label(master)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.bg_frames = []
        bg_gif = Image.open("jarvis.gif")
        for frame in ImageSequence.Iterator(bg_gif):
            frame = frame.resize((720, 560), Image.Resampling.LANCZOS)
            self.bg_frames.append(ImageTk.PhotoImage(frame))

        self.bg_index = 0
        self.bg_running = True
        self.animate_background()

        # Kommentti: Muut käyttöliittymäelementit
        self.label = tk.Label(master, text="🔷 JARVIS Voice Assistant",
                              font=("Consolas", 18, "bold"), fg="#00ffe1", bg="#0f0f0f")
        self.label.pack(pady=10)

        self.chat_display = scrolledtext.ScrolledText(master, width=80, height=10, wrap=tk.WORD,
                                                      font=("Consolas", 10), bg="#1e1e1e", fg="#00ff90",
                                                      insertbackground="white", borderwidth=2, relief="solid")
        self.chat_display.place(relx=0.5, rely=1.0, anchor="s", y=-20)
        self.chat_display.configure(state='disabled')
        self.chat_display.pack(pady=10)

        self.running = True
        self.label.config(text="🔊 Listening for activation phrase...")
        self.listen_thread = threading.Thread(target=self.listen_for_commands)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def animate_background(self):
        if self.bg_running:
            frame = self.bg_frames[self.bg_index]
            self.bg_label.configure(image=frame)
            self.bg_index = (self.bg_index + 1) % len(self.bg_frames)
            self.master.after(100, self.animate_background)

    def stop_background_animation(self):
        self.bg_running = False  # Kommentti: Pysäytetään animaatio

    def log_message(self, role, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{role}: {message}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def listen_for_commands(self):
        while self.running:
            try:
                # Kommentti: Kuunnellaan aktivointilausetta
                speak("Activated!")
                self.label.config(text="🎤 Activated. Ready for commands.")
                speak("Listening.")
                self.stop_background_animation()

                while self.running:
                    text = listen_for_speech()
                    if not text:
                        speak("Could not recognize speech.")
                        continue

                    self.label.config(text=f"📝 Recognized: {text}")
                    self.log_message("You", text)

                    if any(exit_word in text for exit_word in ["bye", "shutdown", "exit"]):
                        speak("Goodbye.")
                        self.log_message("Jarvis", "Session ended.")
                        self.label.config(text="🟢 Waiting for activation phrase...")
                        self.bg_running = True
                        break

                    intent = interpret(text)
                    if intent:
                        response = execute_command(intent, text)
                        if response:
                            self.log_message("Jarvis", response)
                    else:
                        speak("I can't understand the command.")
                        self.log_message("Jarvis", "I can't understand the command.")

            except Exception as e:
                print(f"Error: {e}")
                speak("An error occurred.")
                self.label.config(text="⚠ Error. See console.")
                self.log_message("Jarvis", f"Error: {e}")

# Kommentti: Käynnistetään GUI-sovellus
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = JarvisGUI(root)
        root.mainloop()
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()