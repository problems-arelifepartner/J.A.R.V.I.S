import os
import sys
import subprocess

def install(package):
    """Installs a python package using the current python executable's pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("[*] Starting setup for J.A.R.V.I.S...")
    
    # 1. Install necessary dependencies
    dependencies = ["google-generativeai", "colorama"]
    for dep in dependencies:
        try:
            print(f"[*] Installing {dep}...")
            install(dep)
        except Exception as e:
            print(f"[!] Error installing {dep}: {e}")
            print(f"[!] Please try installing it manually using: pip install {dep}")
            
    # 2. Check for api_key.txt
    if not os.path.exists("api_key.txt"):
        print("[*] Creating api_key.txt file...")
        with open("api_key.txt", "w") as f:
            f.write("")
        print("[!] Created empty api_key.txt. Please write your Gemini API key in this file.")
    else:
        print("[*] api_key.txt already exists.")
        
    print("[+] Setup completed successfully. Please update api_key.txt and run jarvis.py")

if __name__ == "__main__":
    main()
