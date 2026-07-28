# Virtual mouse integration README

The virtual mouse feature uses your webcam to track hand gestures and control the system mouse.

Where it runs:
- Desktop Linux/Windows: supported (requires webcam, opencv-python, mediapipe, pyautogui).
- Termux/Android: not supported for direct system control (pyautogui can't control Android UI). The assistant will inform you when the device is unsupported.

How to install (desktop):
- pip install opencv-python mediapipe pyautogui
- Run: python3 jarvis-terminal/virtual_mouse/main.py

How to use via J.A.R.V.I.S:
- Say: "Open virtual mouse" or "start virtual mouse" during a voice session. J.A.R.V.I.S will launch the visualizer window and the system mouse will be controlled by your hand gestures.
