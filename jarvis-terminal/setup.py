#!/usr/bin/env python3
import os
import sys
import subprocess


def main():
    print("[*] Starting setup for J.A.R.V.I.S...")

    # Install from requirements.txt if available
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        try:
            print(f"[*] Installing pip dependencies from {req_file}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        except Exception as e:
            print(f"[!] Error installing from {req_file}: {e}")
            print("[!] You may try: pip install -r requirements.txt")
    else:
        print("[!] requirements.txt not found; installing core packages individually...")
        dependencies = [
            "google-generativeai",
            "openai",
            "colorama",
            "SpeechRecognition",
            "gTTS",
            "term-image",
            "pydub",
            "requests",
        ]
        for dep in dependencies:
            try:
                print(f"[*] Installing {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            except Exception as e:
                print(f"[!] Error installing {dep}: {e}")

    # 2. Check for api_key.txt
    if not os.path.exists("api_key.txt"):
        print("[*] Creating api_key.txt file...")
        with open("api_key.txt", "w") as f:
            f.write("")
        print("[!] Created empty api_key.txt. Please write your Gemini / OpenAI API key in this file or set environment variables.")
    else:
        print("[*] api_key.txt already exists.")

    print("[+] Setup completed. Please set OPENAI_API_KEY or GEMINI_API_KEY or write a key into api_key.txt.")


if __name__ == "__main__":
    main()
