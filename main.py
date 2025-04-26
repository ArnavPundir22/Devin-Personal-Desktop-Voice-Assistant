import sys
import threading
import datetime
import os
import re
import time
import webbrowser
import wikipedia
import psutil
import winsound
import pyautogui
import random
import speech_recognition as sr
import pyttsx3
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

active_mode = True
HOTWORD = "listen"

# Initialize speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

def speak(text):
    if text:
        gui.log_conversation("Assistant", text)
        engine.say(text)
        engine.runAndWait()

def normalize_query(query):
    return re.sub(r'[^\w\s]', '', query.lower()).strip()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Beep before listening
        winsound.Beep(900, 120)

        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        return normalize_query(query)
    except:
        speak("Sorry, I didn’t catch that.")
        return ""

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning Sir!")
    elif 12 <= hour < 16:
        speak("Good afternoon Sir!")
    else:
        speak("Good evening Sir!")
    speak("I am Devin, your desktop AI assistant. How may I help you?")

def casual_talk(query):
    responses = {
        "how are you": "I'm always operational, Sir. How about you?",
        "who are you": "I am Devin, your personal desktop assistant.",
        "what can you do": "I can help you with tasks like opening websites, telling time, searching, and more.",
        "tell me a joke": "Why don't programmers like nature? Because it has too many bugs.",
        "what is your name": "I am Devin. Nice to talk to you.",
        "thank you": "You're always welcome, Sir.",
        "are you real": "As real as software can be!",
        "do you love me": "I admire your coding skills, Sir!",
        "i am good": "I hope that you always remain the same!!",
        "can you do me a favour": "Yes Sir! It's my pleasure to help you, Please tell me how can I help You? "
    }

    for key in responses:
        if key in query:
            speak(responses[key])
            return True
    return False

def listen_for_hotword():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for hotword...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"Hotword check heard: {query}")
        if HOTWORD in normalize_query(query):
            gui.flash_waveform()
            speak("Yes, I'm listening.")
            return True
    except:
        pass
    return False

def set_brightness(level):
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level} percent.")
    except Exception as e:
        speak("Failed to set brightness.")

def extract_percentage(text):
    match = re.search(r'\b(\d{1,3})\b', text)
    if match:
        percent = int(match.group(1))
        return min(100, max(0, percent))  # clamp between 0 and 100
    return None

def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Use scalar volume (0.0 to 1.0)
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)

        speak(f"Volume set to {level} percent.")
    except Exception as e:
        speak("Failed to set volume.")
        print(f"Error: {e}")



def close_application(app_name):
    closed = False
    for proc in psutil.process_iter(['name']):
        try:
            if app_name.lower() in proc.info['name'].lower():
                proc.terminate()
                closed = True
        except:
            pass
    if closed:
        speak(f"{app_name} has been closed.")
    else:
        speak(f"Couldn't find any running instance of {app_name}.")

def close_edge_browser():
    closed_any = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if "msedge.exe" in proc.info['name'].lower():
                proc.terminate()
                closed_any = True
        except:
            pass
    if closed_any:
        speak("Microsoft Edge has been closed.")
    else:
        speak("Microsoft Edge is not running.")

def control_media(command):
    if "pause" in command or "play" in command:
        pyautogui.press("playpause")
        speak("Toggling play/pause")
    elif "next" in command:
        pyautogui.press("nexttrack")
        speak("Skipping to next")
    elif "previous" in command:
        pyautogui.press("prevtrack")
        speak("Going to previous")
    elif "volume up" in command:
        pyautogui.press("volumeup")
        speak("Increasing volume")
    elif "volume down" in command:
        pyautogui.press("volumedown")
        speak("Decreasing volume")

def handle_command(query):
    if "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")


    elif "set brightness to" in query:
        level = extract_percentage(query)
        if level is not None:
            set_brightness(level)
        else:
            speak("Please specify a brightness level from 0 to 100.")

    elif "set volume to" in query:
        level = extract_percentage(query)
        if level is not None:
            set_volume(level)
        else:
            speak("Please specify a volume level from 0 to 100.")

    elif "open chat gpt" in query:
        webbrowser.open("https://www.chatgpt.com")
        speak("Opening ChatGPT")

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif "play" in query and "on youtube" in query:
        search_term = query.replace("play", "").replace("on youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
        webbrowser.open(url)
        speak(f"Playing {search_term} on YouTube")
        time.sleep(6)
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")

    elif any(media in query for media in ["pause", "play", "next", "previous", "volume up", "volume down"]):
        control_media(query)

    elif "search for" in query:
        search_term = query.replace("search for", "").strip()
        url = f"https://www.google.com/search?q={search_term}"
        webbrowser.open(url)
        speak(f"Searching Google for {search_term}")
# ================================================================
# Project: Devin - Personal DEsktop Assistant
# Author: Arnav Pundir
# Year: 2025
# License: Custom Proprietary License - All Rights Reserved
# Unauthorized use, copying, or distribution is strictly prohibited.
# ================================================================
    elif "wikipedia" in query:
        try:
            topic = query.replace("wikipedia", "").strip()
            result = wikipedia.summary(topic, sentences=2)
            speak(f"According to Wikipedia: {result}")
        except:
            speak("Sorry, I couldn't find anything on Wikipedia.")



    elif "open notepad" in query:
        os.system("notepad.exe")
        speak("Opening Notepad")

    elif "close notepad" in query:
        close_application("notepad.exe")

    elif "close edge" in query or "close browser" in query:
        close_edge_browser()

    elif "close" in query:
        app_name = query.replace("close", "").strip()
        if app_name:
            close_application(app_name + ".exe")
        else:
            speak("Please specify which app you want to close.")
# ================================================================
# Project: Devin - Personal Desktop Voice Assistant
# Author: Arnav Pundir
# Year: 2025
# License: Custom Proprietary License - All Rights Reserved
# Unauthorized use, copying, or distribution is strictly prohibited.
# ================================================================
    elif "exit" in query or "quit" in query or "band ho ja" in query:
        speak("Goodbye Sir! Call me when you need me again.")
        sys.exit()

    elif casual_talk(query):
        pass
    else:
        speak("I didn't understand that. Try something else.")

def assistant_loop():
    global active_mode
    greet_user()
    while True:
        if active_mode:
            command = take_command()
            if command:
                gui.log_conversation("You", command)
                if "shut up" in command or "stop listening" in command:
                    speak("Okay, going into standby. Say 'listen' to wake me up.")
                    active_mode = False
                else:
                    handle_command(command)
            else:
                speak("Could you please repeat that?")
        else:
            if listen_for_hotword():
                active_mode = True




class DevinGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Devin - AI Desktop Assistant")
        self.setGeometry(100, 100, 600, 550)
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #FFFFFF; font-family: 'Segoe UI'; }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #00bcd4;
                color: white;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #00bcd4;
                color: white;
                padding: 6px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #00bcd4;
                color: black;
                font-weight: bold;
                padding: 6px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00e5ff;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("🔊 Devin is Listening...")
        self.status_label.setFont(QFont("Arial", 20))
        self.status_label.setAlignment(Qt.AlignCenter)

        self.waveform_label = QLabel("-")
        self.waveform_label.setFont(QFont("Consolas", 28))
        self.waveform_label.setAlignment(Qt.AlignCenter)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type a command...")
        self.command_input.returnPressed.connect(self.process_text_command)

        self.submit_button = QPushButton("Send")
        self.submit_button.clicked.connect(self.process_text_command)

        layout.addWidget(self.status_label)
        layout.addWidget(self.waveform_label)
        layout.addWidget(self.console)
        layout.addWidget(self.command_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        self.waveform_timer = QTimer()
        self.waveform_timer.timeout.connect(self.animate_waveform)
        self.waveform_timer.start(300)

        self.wave_height = 5
        self.wave_direction = 1

    def animate_waveform(self):
        wave = ""
        for i in range(10):
            height = self.wave_height if i % 2 == 0 else self.wave_height - 1
            wave += f"{'|' * height} "
        self.waveform_label.setText(wave)

        if self.wave_height >= 8:
            self.wave_direction = -1
        elif self.wave_height <= 3:
            self.wave_direction = 1

        self.wave_height += self.wave_direction

    def log_conversation(self, sender, text):
        self.console.append(f"{sender}: {text}")

    def process_text_command(self):
        command = self.command_input.text().strip()
        if command:
            self.log_conversation("You", command)
            self.command_input.clear()
            self.status_label.setText("💬 Responding...")
            handle_command(command)
            QTimer.singleShot(2000, lambda: self.status_label.setText("🔊 Devin is Listening..."))

    def flash_waveform(self):
        self.waveform_label.setStyleSheet("color: #00ffcc;")
        QTimer.singleShot(500, lambda: self.waveform_label.setStyleSheet("color: white;"))

    def animate_typing_response(self, text):
        self.console.moveCursor(self.console.textCursor().End)
        self.console.insertPlainText("Assistant: ")
        self._typing_index = 0
        self._typing_text = text
        self._typing_timer = QTimer()
        self._typing_timer.timeout.connect(self._type_next_char)
        self._typing_timer.start(30)

    def _type_next_char(self):
        if self._typing_index < len(self._typing_text):
            self.console.insertPlainText(self._typing_text[self._typing_index])
            self._typing_index += 1
        else:
            self._typing_timer.stop()
            self.console.insertPlainText("\n")
# Start GUI and Assistant
app = QApplication(sys.argv)
gui = DevinGUI()
gui.show()

assistant_thread = threading.Thread(target=assistant_loop)
assistant_thread.daemon = True
assistant_thread.start()

sys.exit(app.exec_())
