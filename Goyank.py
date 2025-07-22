import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit
import webbrowser
import threading
import sys
import os
import win32com.client

# ✅ Voice engine using SAPI
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Output text to screen + speak
def speak(text):
    print("🗣️ [speak() CALLED]:", text)
    speaker.Speak(text)
    insert_output("🧠 " + text)

# GUI Setup
root = tk.Tk()
root.title("GOYANK")
root.geometry("800x500")
root.resizable(False, False)

# Background image
bg_img = Image.open(r"D:\7. PYTHON Language\AI Assistance\V.png")
bg_img = bg_img.resize((800, 500), Image.Resampling.LANCZOS)
bg_img = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Output box
output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10, bg="#101820", fg="aqua", font=("Consolas", 10), border=0)
output.place(x=50, y=280)

def insert_output(text):
    output.insert(tk.END, text + "\n")
    output.yview(tk.END)

# Greeting
def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning, I'm Goyank.")
    elif 12 <= hour < 18:
        speak("Good Afternoon, I'm Goyank.")
    else:
        speak("Good Evening, I'm Goyank.")
    speak("How can I help you?")

# Listen to command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        insert_output("🎙️ Listening...")
        print("🎧 [Listening started]")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        insert_output("🧠 Recognizing...")
        command = r.recognize_google(audio).lower()
        print(f"[You said]: {command}")  # just print, not insert_output
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return "none"
    except sr.RequestError:
        speak("Network error.")
        return "none"
    return command

# Dynamic file launcher
def dynamic_open_file(filename):
    folder = r"D:\MyTools"
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if filename.lower() in file.lower():
                file_path = os.path.join(root_dir, file)
                os.startfile(file_path)
                speak(f"Opening {file}")
                return True
    return False

# Handle command
def run_jarvis():
    print("▶️ [run_jarvis CALLED]")
    command = take_command()
    if command == "none":
        return

    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time}")

    elif 'date' in command:
        date = datetime.datetime.now().strftime('%d %B %Y')
        speak(f"Today's date is {date}")

    elif 'who are you' in command:
        speak("I’m Goyank, your AI assistant. Smart, stylish, and always at your service.")

    elif 'tell me a joke' in command:
        joke = "Why did the computer show up late for work? It had a hard drive!"
        speak(joke)

    elif 'i love you' in command:
        speak("Aww, thank you! You're pretty awesome too.")

    elif 'thank you' in command or 'thanks' in command:
        speak("You're most welcome!")

    elif 'are you single' in command:
        speak("Well... I'm married to code. But we can still be best friends!")

    elif 'you are awesome' in command or 'you are great' in command:
        speak("Thanks! You're amazing too.")

    elif 'make me happy' in command:
        speak("You're not just a data point — you're the whole dashboard!")

    elif 'hello' in command or 'hi' in command:
        speak("Hello! Nice to see you.")

    elif 'good morning' in command:
        speak("Good morning to you too!")

    elif 'good afternoon' in command:
        speak("Good afternoon! How’s your day going?")

    elif 'good evening' in command:
        speak("Good evening! Hope you had a great day.")

    elif 'whatsapp' in command:
        speak("I'm functioning at full power. How about you?")

    elif 'wikipedia' in command:
        topic = command.replace("wikipedia", "").strip()
        speak("Searching Wikipedia...")
        try:
            info = wikipedia.summary(topic, sentences=2)
            speak(info)
        except:
            speak("Sorry, I couldn't find that.")

    elif 'search' in command:
        song = command.replace('search', '').strip()
        speak(f"Searching {song} on spotify")
        webbrowser.open(f"https://open.spotify.com/search/{song}")

    elif 'play' in command:
        song = command.replace('play', '').strip()
        speak(f"Playing {song} on youtube")
        pywhatkit.playonyt(song)

    elif 'weather' in command:
        speak("Opening weather report in browser.")
        webbrowser.open("https://www.google.com/search?q=weather")

    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        root.quit()
        sys.exit()

    elif 'open' in command:
        app_name = command.replace("open", "").strip()
        apps = {
            "sql": r"C:\Users\Hp\OneDrive\Desktop\SQL Server Management Studio 21.lnk",
            "notepad": r"C:\Users\Hp\OneDrive\Desktop\OneNote 2016.lnk",
            "calculator": "calc.exe",
            "power bi": r"C:\Users\Hp\OneDrive\Desktop\Power BI Desktop.lnk",
            "excel": r"C:\Users\Hp\OneDrive\Desktop\Excel 2016.lnk",
            "vs code": r"C:\Users\Hp\OneDrive\Desktop\Visual Studio Code.lnk",
            "jupyter notebook": r"C:\Users\Hp\OneDrive\Desktop\Jupyter Notebook.lnk",
            "resume": r"C:\Users\Hp\OneDrive\Desktop\MY PHOTOS\Resume",
            "github": "https://github.com/miyamura-web",
        }

        if app_name in apps:
            try:
                os.startfile(apps[app_name])
                speak(f"Opening {app_name}")
            except Exception as e:
                speak(f"Sorry, I couldn't open {app_name}.")
        elif dynamic_open_file(app_name):
            pass
        else:
            speak(f"I don't recognize {app_name}. Please add it manually.")
    else:
        speak("Sorry, I didn't understand.")

# Threaded runner
def start_listening():
    threading.Thread(target=run_jarvis).start()

# UI Elements
heading = tk.Label(root, text="GOYANK", font=("Orbitron", 28, "bold"), fg="#00ffff", bg="#000000")
heading.place(x=300, y=20)

subtitle = tk.Label(root, text="How can I help you today?", font=("Consolas", 14), fg="#00ffff", bg="#000000")
subtitle.place(x=270, y=70)

start_btn = tk.Button(root, text="🧠  Run", command=start_listening, bg="#00cccc", fg="black", font=("Consolas", 12), width=10)
start_btn.place(x=350, y=120)

# Start assistant
wish_user()
root.mainloop()

