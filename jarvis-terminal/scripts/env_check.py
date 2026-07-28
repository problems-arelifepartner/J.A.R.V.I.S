#!/usr/bin/env python3
"""
Environment checker — prints which optional and required Python packages are available and
prints actionable instructions to install missing ones. Run this before trying to run J.A.R.V.I.S.
"""
import importlib
import sys

packages = [
    "openai",
    "google.generativeai",
    "speech_recognition",
    "gtts",
    "term_image",
    "pydub",
    "requests",
    "opencv_python",
    "cv2",
    "mediapipe",
    "pyautogui",
    "colorama",
    "whisper",
    "gpt4all",
    "llama_cpp",
]

print("J.A.R.V.I.S Environment Check")
print("Python:", sys.version)
print()
missing = []
for pkg in packages:
    name = pkg
    try:
        # special-case cv2 import name
        if pkg == "opencv_python":
            import cv2 as _mod
        else:
            importlib.import_module(pkg)
        print(f"[OK] {pkg}")
    except Exception:
        print(f"[MISSING] {pkg}")
        missing.append(pkg)

if missing:
    print()
    print("Missing packages detected. Try installing the most important ones:")
    print("pip install -r requirements.txt")
    print("If opencv/mediapipe fails on your platform, consult their platform-specific installation guides.")
else:
    print()
    print("All listed packages appear importable. You should be able to run J.A.R.V.I.S and the virtual mouse.")
