import os
import sys
import subprocess
import time

def run_command(command, use_sudo=False):
    """Executes a shell command safely, appending sudo if required by the OS."""
    if use_sudo and not is_termux():
        command = f"sudo {command}"
    
    print(f"\n[*] Executing: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Critical Error: Command failed with exit code {e.returncode}.")
        print("Please check your internet connection or permissions and try again.")
        sys.exit(1)

def is_termux():
    """Detects if the script is running inside Android's Termux environment."""
    return "TERMUX_VERSION" in os.environ

def install_system_dependencies():
    """Phase 1: Installs OS-level C-compilers and audio mixer binaries."""
    print("\n--- Phase 1: System Dependencies ---")
    
    if is_termux():
        print("[i] Android / Termux environment detected.")
        # clang and portaudio are strictly required to compile PyAudio in Termux
        run_command("pkg update && pkg upgrade -y")
        run_command("pkg install python clang portaudio ffmpeg termux-api mpv -y")
        
    elif sys.platform.startswith("linux"):
        print("[i] Linux (Ubuntu/Debian) environment detected.")
        # portaudio19-dev and libasound2-dev are required for PyAudio on Linux
        run_command("apt update", use_sudo=True)
        run_command("apt install python3-pip python3-dev portaudio19-dev libasound2-dev ffmpeg mpv -y", use_sudo=True)
        
    else:
        print("[!] Unsupported operating system. This script supports Linux and Termux.")
        sys.exit(1)

def install_python_packages():
    """Phase 2: Installs all required Python modules via pip."""
    print("\n--- Phase 2: Python Packages ---")
    
    # pocketsphinx is included here so your offline wake-word works out-of-the-box
    packages = "google-generativeai speechrecognition gTTS pyaudio pocketsphinx"
    
    # Use sys.executable to ensure we use the pip associated with the current Python environment
    run_command(f"{sys.executable} -m pip install {packages} --upgrade")

def initialize_engine():
    """Phase 3: Validates environment variables and launches J.A.R.V.I.S."""
    print("\n--- Phase 3: Engine Initialization ---")
    
    # Check for API key. If missing, prompt the user so it doesn't crash on boot.
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n[!] GEMINI_API_KEY is missing from your environment variables.")
        api_key = input("Please paste your Gemini API Key now: ").strip()
        
        if not api_key:
            print("[!] Boot sequence aborted: J.A.R.V.I.S. requires an API key to function.")
            sys.exit(1)
            
        # Inject the key into the runtime environment for jarvis.py to find
        os.environ["GEMINI_API_KEY"] = api_key

    print("\n[+] All systems green. Booting J.A.R.V.I.S. core...")
    time.sleep(1.5) # Slight delay for dramatic effect / readability
    
    try:
        # Launch the main application loop
        subprocess.run([sys.executable, "jarvis.py"], check=True)
    except KeyboardInterrupt:
        print("\n[i] Engine initialization interrupted by user.")
    except FileNotFoundError:
        print("\n[!] Error: 'jarvis.py' not found in the current directory.")
        print("Make sure you are running this setup script from the project root.")
    except Exception as e:
        print(f"\n[!] Boot sequence failed: {e}")

if __name__ == "__main__":
    print("===========================================")
    print("  J.A.R.V.I.S. Automated Setup & Launcher  ")
    print("===========================================")
    
    install_system_dependencies()
    install_python_packages()
    initialize_engine()
