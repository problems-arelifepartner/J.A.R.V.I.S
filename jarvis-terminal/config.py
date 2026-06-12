import os
import sys
import shutil

class Config:
    def __init__(self):
        # 1. Detect Environment
        self.is_termux = "TERMUX_VERSION" in os.environ
        self.is_linux = sys.platform.startswith("linux") and not self.is_termux
        
        # 2. Load API Key
        self.api_key = self.load_api_key()
            
        # 3. Validate System Dependencies
        self.validate_dependencies()

    def load_api_key(self):
        """Reads the user's API key from the local file."""
        try:
            with open("api_key.txt", "r") as f:
                key = f.read().strip()
                if not key:
                    raise ValueError("API key file is empty.")
                return key
        except (FileNotFoundError, ValueError):
            print("[ERROR] Missing or empty 'api_key.txt'.")
            print("Please run 'python setup.py' to configure your API key.")
            sys.exit(1)

    def validate_dependencies(self):
        required_commands = ["mpv"] if not self.is_termux else ["termux-tts-speak"]
        for cmd in required_commands:
            if not shutil.which(cmd):
                print(f"[WARNING] Missing system dependency: '{cmd}'. Some voice functions may fail.")
