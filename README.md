# Devin - AI Desktop Assistant

Devin is a Python-based desktop AI assistant that offers voice and text control over various system functionalities and web interactions. It comes with a modern PyQt5 GUI, natural language processing via Google's Speech Recognition API, and text-to-speech responses using `pyttsx3`. Devin also supports brightness and volume adjustments, browser interactions, and application control.

---

## Creator
**Developed by:** *Arnav Pundir* , *Atharv kumar* and *Aman Bhatti*

---

## Features

- 🎤 **Voice Command Activation**: Say "listen" to activate listening mode.
- 🧠 **Natural Language Understanding**: Responds to casual and functional queries.
- 💬 **GUI Command Console**: Type and execute commands directly from the GUI.
- 📦 **Web Automation**: Opens Google, YouTube, ChatGPT, and more.
- 🔊 **System Volume Control**: Adjust system volume using voice.
- 💡 **Brightness Control**: Set screen brightness from 0% to 100%.
- 🖥 **App Control**: Open and close apps like Notepad and Microsoft Edge.
- 📺 **Media Playback Control**: Pause, play, skip, and adjust volume.
- 🤖 **Joke & Casual Talk**: Interact casually for a friendly experience.

---

## Installation

### Prerequisites
- Python 3.7+

### Required Packages
Install the required dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` should include:
```txt
pyqt5
pyttsx3
speechrecognition
wikipedia
pyautogui
psutil
screen-brightness-control
pycaw
comtypes
```

---

## How to Use

### Launch Devin
```bash
python devin.py
```

### Modes of Interaction
- **Voice Mode**: Activated by saying "listen"
- **Text Mode**: Type commands in the GUI text input

### Supported Voice Commands
- "What is the time"
- "Open Google/YouTube/ChatGPT"
- "Set brightness to 50"
- "Set volume to 30"
- "Search for Python tutorials"
- "Play lo-fi on YouTube"
- "Close notepad/edge/browser"
- "Exit" or "Quit"
- Casual phrases: "Tell me a joke", "Who are you?", etc.

---

## Project Structure
```
Devin_Assistant/
├── devin.py               # Main application file
├── README.md              # Project overview and usage
├── requirements.txt       # Python dependencies
```

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License
MIT License

---

## Acknowledgements
- [PyQt5](https://pypi.org/project/PyQt5/)
- [Google Speech Recognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [Wikipedia API](https://pypi.org/project/wikipedia/)
- [pyautogui](https://pypi.org/project/PyAutoGUI/)
- [pycaw](https://github.com/AndreMiras/pycaw)

---

_Enjoy using Devin!_

