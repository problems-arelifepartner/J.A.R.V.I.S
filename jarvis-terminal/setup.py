import os
import sys
import subprocess
import time

def run_command(command, use_sudo=False, capture_error=False):
    """Executes a shell command safely, appending sudo if required by the OS."""
    if use_sudo and not is_termux():
        command = f"sudo {command}"
    
    print(f"\n[*] Executing: {command}")
    try:
        # If capture_error is True, we suppress the crash so the script can attempt a fallback
        if capture_error:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        if not capture_error:
            print(f"\n[!] Critical Error: Command failed with exit code {e.returncode}.")
            sys.exit(1)
        return False

def is_termux():
    """Detects if the script is running inside Android's Termux environment."""
    return "TERMUX_VERSION" in os.environ

def install_system_dependencies():
    """Phase 1: Installs comprehensive OS-level tools to prevent C-compiler errors."""
    print("\n--- Phase 1: Deep System Dependencies ---")
    
    if is_termux():
        print("[i] Android / Termux environment detected.")
        # Added ndk-sysroot, binutils, and swig to prevent PocketSphinx and PyAudio build errors
        run_command("pkg update && pkg upgrade -y")
        run_command("pkg install python clang portaudio ffmpeg termux-api mpv swig binutils ndk-sysroot make -y")
        
    elif sys.platform.startswith("linux"):
        print("[i] Linux (Ubuntu/Debian) environment detected.")
        # Added build-essential, swig, and pkg-config to cover almost all C-extension compile errors
        run_command("apt-get update", use_sudo=True)
        packages = "python3-pip python3-dev portaudio19-dev libasound2-dev ffmpeg mpv swig build-essential pkg-config"
        run_command(f"apt-get install {packages} -y", use_sudo=True)
        
    else:
        print("[!] Unsupported operating system. This script supports Linux and Termux.")
        sys.exit(1)

def install_python_packages():
    """Phase 2: Resilient Python package installation with fallback mechanisms."""
    print("\n--- Phase 2: Python Packages ---")
    
    # 1. First, upgrade pip and core build tools. 
    # Failing to do this is the #1 cause of wheel-building errors.
    print("\n[i] Upgrading core build modules (pip, setuptools, wheel)...")
    run_command(f"{sys.executable} -m pip install --upgrade pip setuptools wheel")

    # 2. Itemized installation of primary dependencies
    packages = [
        "google-generativeai", 
        "speechrecognition", 
        "gTTS", 
        "pyaudio", 
        "pocketsphinx"
    ]
    
    print("\n[i] Installing application dependencies...")
    for pkg in packages:
        print(f"\n[*] Attempting to install: {pkg}")
        success = run_command(f"{sys.executable} -m pip install {pkg}", capture_error=True)
        
        # 3. Fallback Logic: If standard install fails, try aggressive fallback
        if not success:
            print(f"[!] Standard install failed for {pkg}. Attempting aggressive fallback...")
            
            # Fallback attempts: clear cache, force re-compilation
            fallback_cmd = f"{sys.executable} -m pip install {pkg} --no-cache-dir --force-reinstall"
            fallback_success = run_command(fallback_cmd, capture_error=True)
            
            if not fallback_success:
                print(f"\n[!!!] FATAL: Unable to install {pkg} even with fallback methods.")
                print("This usually means your OS is missing a specific C-header required by this library.")
                sys.exit(1)
            else:
                print(f"[+] Fallback successful. {pkg} installed.")

def initialize_engine():
    """Phase 3: Validates environment variables and launches J.A.R.V.I.S."""
    print("\n--- Phase 3: Engine Initialization ---")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n[!] GEMINI_API_KEY is missing from your environment variables.")
        api_key = input("Please paste your Gemini API Key now: ").strip()
        
        if not api_key:
            print("[!] Boot sequence aborted: J.A.R.V.I.S. requires an API key to function.")
            sys.exit(1)
            
        os.environ["GEMINI_API_KEY"] = api_key

    print("\n[+] Setup complete. All systems green. Booting J.A.R.V.I.S. core...")
    time.sleep(1.5) 
    
    try:
        subprocess.run([sys.executable, "jarvis.py"], check=True)
    except KeyboardInterrupt:
        print("\n[i] Engine initialization interrupted by user.")
    except FileNotFoundError:
        print("\n[!] Error: 'jarvis.py' not found in the current directory.")
    except Exception as e:
        print(f"\n[!] Boot sequence failed: {e}")

if __name__ == "__main__":
    print("===========================================")
    print("  J.A.R.V.I.S. Automated Setup & Launcher  ")
    print("===========================================")
    
    install_system_dependencies()
    install_python_packages()
    initialize_engine()
