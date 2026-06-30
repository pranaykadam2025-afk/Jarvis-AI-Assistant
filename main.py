import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibraey
import requests
from google import genai

# -------------------- CONFIG --------------------
NEWS_API = "f614612a44e4475c93e12299297cd76e"

client = genai.Client(
    api_key="YOUR_GEMINI_API_KEY"
)

recognizer = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty("rate", 170)

# ---------------- SPEAK ----------------
def speak(text):
    text = str(text)
    print("Jarvis:", text)

    engine.stop()  # Previous speech stop karo

    # Long text ko chhote parts me bolo
    for line in text.split("."):
        if line.strip():
            engine.say(line.strip())
            engine.runAndWait()


# ---------------- GEMINI ----------------
def aiProcess(command):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=command
        )
        return response.text

    except Exception as e:
        error = str(e)

        if "429" in error or "RESOURCE_EXHAUSTED" in error:
            return "Sorry Sir, my Gemini API quota has been exhausted. Please try again later."

        return f"Sorry Sir, an error occurred: {error}"

# ---------------- COMMANDS ----------------
def processCommand(command):

    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play"):

        song = command.replace("play", "").strip()

        link = musicLibraey.music.get(song)

        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Song not found.")

    elif "news" in command:

        speak("Fetching today's headlines.")

        try:
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API}"
            )

            if r.status_code == 200:

                data = r.json()

                articles = data.get("articles", [])

                if not articles:
                    speak("No news found.")
                else:
                    for article in articles[:5]:
                        title = article["title"]
                        print(title)
                        speak(title)

            else:
                speak("Unable to fetch news.")

        except Exception as e:
            print(e)
            speak("Something went wrong.")

    elif "exit" in command or "stop" in command:
        speak("Goodbye Sir")
        exit()

    else:
            answer = aiProcess(command)

    print("Length:", len(answer))
    print(answer)

    speak(answer)


# ---------------- MAIN ----------------
speak("Jarvis is online.")

while True:

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print("\nWaiting for wake word...")

            audio = recognizer.listen(source)

        wake = recognizer.recognize_google(
            audio,
            language="en-IN"
        ).lower()

        print("Wake:", wake)

        if "jarvis" in wake:

            speak("Yes sir")

            with sr.Microphone() as source:

                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("Listening...")

                audio = recognizer.listen(source)

            command = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("Command:", command)

            processCommand(command)

    except sr.UnknownValueError:
        continue

    except KeyboardInterrupt:
        break

    except Exception as e:
        print("Error:", e)