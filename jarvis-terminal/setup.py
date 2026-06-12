import os
import sys
import subprocess
import time

def run_command(command, use_sudo=False, capture_error=False):
    if use_sudo and not is_termux():
        command = f"sudo {command}"
    try:
        # We will now show the logs so it doesn't look stuck
        if capture_error:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def is_termux():
    return "TERMUX_VERSION" in os.environ

def install_system_dependencies():
    print("\n--- Phase 1: Deep System Dependencies ---")
    if is_termux():
        run_command("pkg update && pkg upgrade -y")
        run_command("pkg install python clang portaudio ffmpeg termux-api mpv swig binutils ndk-sysroot make -y")
    elif sys.platform.startswith("linux"):
        run_command("apt-get update", use_sudo=True)
        packages = "python3-pip python3-dev portaudio19-dev libasound2-dev ffmpeg mpv swig build-essential pkg-config"
        run_command(f"apt-get install {packages} -y", use_sudo=True)

def install_python_packages():
    print("\n--- Phase 2: Python Packages ---")
    
    # FIX 1: Removed 'pip' from this line so Termux doesn't throw the yellow warning!
    run_command(f"{sys.executable} -m pip install --upgrade setuptools wheel")
    
    packages = ["google-generativeai", "speechrecognition", "gTTS", "pyaudio", "pocketsphinx", "term-image"]
    
    for pkg in packages:
        print(f"\n[*] Installing {pkg}... (Please wait, this can take a few minutes on Android)")
        
        # FIX 2: capture_error is now set to False. You will see a massive wall of text scrolling. 
        # This is GOOD. It means it is working and not stuck!
        success = run_command(f"{sys.executable} -m pip install {pkg}", capture_error=False)
        
        if not success:
            print(f"[!] Fallback triggered for {pkg}...")
            run_command(f"{sys.executable} -m pip install {pkg} --no-cache-dir --force-reinstall", capture_error=False)

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

    # Automatically protect the user from uploading it to GitHub
    gitignore_entry = "api_key.txt\n"
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write(gitignore_entry)
    else:
        with open(".gitignore", "r") as f:
            content = f.read()
        if "api_key.txt" not in content:
            with open(".gitignore", "a") as f:
                f.write(f"\n{gitignore_entry}")

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
