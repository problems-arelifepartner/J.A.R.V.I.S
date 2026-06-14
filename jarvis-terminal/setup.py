import os
import sys
import subprocess
import time

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_system_dependencies():
    print("\n--- Phase 1: Installing Termux Dependencies ---")
    run_command("pkg update && pkg upgrade -y")
    run_command("pkg install python clang portaudio ffmpeg termux-api mpv swig binutils ndk-sysroot make pkg-config -y")

def install_python_packages():
    print("\n--- Phase 2: Python Packages ---")
    break_flag = " --break-system-packages"
    
    run_command(f"{sys.executable} -m pip install --upgrade setuptools wheel{break_flag}")
    run_command(f"{sys.executable} -m pip install pydantic-core==2.27.2 --prefer-binary{break_flag}")

    packages = ["pydantic", "google-genai", "speechrecognition", "gTTS", "pyaudio", "pocketsphinx", "term-image"]

    for pkg in packages:
        print(f"\n[*] Installing {pkg} on Termux...")
        success = run_command(f"{sys.executable} -m pip install {pkg} --prefer-binary{break_flag}")

        if not success:
            print(f"[!] Fallback triggered for {pkg}...")
            run_command(f"{sys.executable} -m pip install {pkg} --no-cache-dir --force-reinstall{break_flag}")

def setup_api_key():
    print("\n--- Phase 3: API Configuration ---")
    if not os.path.exists("api_key.txt"):
        print("To use J.A.R.V.I.S., you need a free Gemini API key from Google AI Studio.")
        api_key = input("Please paste your Gemini API Key here: ").strip()

        if not api_key:
            print("[!] Boot sequence aborted: J.A.R.V.I.S. requires an API key to function.")
            sys.exit(1)

        with open("api_key.txt", "w") as f:
            f.write(api_key)
        print("[+] API key saved locally to 'api_key.txt'.")
    else:
        print("[+] Local 'api_key.txt' found.")

def initialize_engine():
    print("\n[+] Setup complete. All systems green. Booting J.A.R.V.I.S. core...")
    time.sleep(1)
    try:
        subprocess.run([sys.executable, "jarvis.py"], check=True)
    except Exception as e:
        print(f"\n[!] Boot sequence failed: {e}")

if __name__ == "__main__":
    install_system_dependencies()
    install_python_packages()
    setup_api_key()
    initialize_engine()
