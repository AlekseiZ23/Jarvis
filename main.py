from wakeword import WakeWordDetector
from stt import listen_for_speech
from tts import speak
from nlu import interpret
from commands import execute_command

# Kommentti: Sovelluksen päätoiminto

def main():
    speak("Assistant started.")
    wake = WakeWordDetector()

    while True:
        try:
            wake.wait_for_wake_word()
            speak("Listening.")

            text = listen_for_speech()
            if text:
                print(f"Recognized: {text}")
                intent_data = interpret(text)

                if intent_data:
                    execute_command(intent_data, text)
                else:
                    speak("I can't understand the command.")
            else:
                speak("Could not recognize speech.")

        except KeyboardInterrupt:
            speak("Shutting down.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("An error occurred, please try again.")

# Kommentti: Suoritetaan päätoiminto, jos tiedosto ajetaan suoraan
if __name__ == "__main__":
    main()