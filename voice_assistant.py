import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import subprocess


# Initialize voice engine
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)


def speak(text):
    print("Assistant:", text)

    engine.say(text)
    engine.runAndWait()


def take_command():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening... Speak now.")

            recognizer.adjust_for_ambient_noise(
                source, duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=6
            )

        print("Recognizing speech...")

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You:", command)
        return command.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return ""

    except sr.RequestError:
        speak("Internet connection or recognition service error.")
        return ""

    except Exception as error:
        print("Microphone error:", error)
        return ""


def process_command(command):

    if not command:
        return True

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    elif "your name" in command:
        speak("I am your Python voice assistant.")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )
        speak("The current time is " + current_time)

    elif "date" in command:
        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )
        speak("Today's date is " + current_date)

    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "open notepad" in command:
        speak("Opening Notepad.")
        subprocess.Popen(["notepad.exe"])

    elif "help" in command:
        speak(
            "You can ask me the time, date, "
            "or tell me to open Google or YouTube."
        )

    elif any(word in command for word in [
        "exit", "goodbye", "stop assistant"
    ]):
        speak("Goodbye! Have a nice day.")
        return False

    else:
        speak("Sorry, I don't know that command yet.")

    return True


def main():
    speak("Hello! I am your Python voice assistant.")
    speak("How can I help you?")

    while True:
        command = take_command()

        if command:
            if not process_command(command):
                break

    engine.stop()
    print("Program closed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        engine.stop()
        print("\nAssistant stopped by keyboard.")
    except Exception as error:
        print("Program error:", error)
        engine.stop()
