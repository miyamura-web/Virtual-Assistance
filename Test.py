import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit
import webbrowser
import threading
import queue
import sys

# ✅ Queue for speech (thread-safe)
speech_queue = queue.Queue()

# ✅ Initialize pyttsx3 with SAPI5 (Windows only)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = Male, 1 = Female
engine.setProperty('rate', 150)

# ✅ TTS Function with debug
def speak(text):
    print("🗣️ [speak() CALLED]:", text)
    speech_queue.put(text)

# ✅ Run queue from main thread
def process_speech_queue():
    while not speech_queue.empty():
        text = speech_queue.get()
        print("🔄 [process_speech_queue RUNNING]:", text)
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("❌ TTS Error:", e)
    root.after(100, process_speech_queue)

# GUI Setup
root = tk.Tk()
root.title("TANJIRO")
root.geometry("800x500")
root.resizable(False, False)

# Background image
bg_img = Image.open(r"D:\7. PYTHON Language\AI Assistance\Image.jpeg")
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
        speak("Good Morning, I'm Tanjiro.")
    elif 12 <= hour < 18:
        speak("Good Afternoon, I'm Tanjiro.")
    else:
        speak("Good Evening, I'm Tanjiro.")
    speak("How can I help you?")
    insert_output("🔵 Tanjiro is online. Click 'Run' and speak your command.")

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
        insert_output(f"🗣️ You said: {command}")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        insert_output("❗ Didn't catch that. Please try again.")
        return "none"
    except sr.RequestError:
        speak("Network error.")
        insert_output("❗ Network error while recognizing.")
        return "none"
    return command

# Handle command
def run_jarvis():
    print("▶️ [run_jarvis CALLED]")
    command = take_command()
    if command == "none":
        return

    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time}")
        insert_output(f"🕒 Time: {time}")
    elif 'date' in command:
        date = datetime.datetime.now().strftime('%d %B %Y')
        speak(f"Today's date is {date}")
        insert_output(f"📅 Date: {date}")
    elif 'wikipedia' in command:
        topic = command.replace("wikipedia", "").strip()
        speak("Searching Wikipedia...")
        insert_output(f"🔍 Wikipedia search: {topic}")
        try:
            info = wikipedia.summary(topic, sentences=2)
            speak(info)
            insert_output(f"📚 {info}")
        except:
            speak("Sorry, I couldn't find that.")
            insert_output("❌ Wikipedia search failed.")
    elif 'play' in command:
        song = command.replace('play', '').strip()
        speak(f"Playing {song} on YouTube")
        insert_output(f"🎵 Playing: {song}")
        pywhatkit.playonyt(song)
    elif 'weather' in command:
        speak("Opening weather report in browser.")
        insert_output("🌦️ Opening weather...")
        webbrowser.open("https://www.google.com/search?q=weather")
    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        insert_output("👋 Session ended.")
        root.quit()
        sys.exit()
    else:
        speak("Sorry, I didn't understand.")
        insert_output("🤖 Command not recognized.")

# Threaded runner
def start_listening():
    threading.Thread(target=run_jarvis).start()

# UI Elements
heading = tk.Label(root, text="TANJIRO", font=("Orbitron", 28, "bold"), fg="#00ffff", bg="#000000")
heading.place(x=300, y=20)

subtitle = tk.Label(root, text="How can I help you today?", font=("Consolas", 14), fg="#00ffff", bg="#000000")
subtitle.place(x=270, y=70)

start_btn = tk.Button(root, text="🧠  Run", command=start_listening, bg="#00cccc", fg="black", font=("Consolas", 12), width=10)
start_btn.place(x=350, y=120)



# Start speech processor
process_speech_queue()

# Start the app
wish_user()
root.mainloop()


