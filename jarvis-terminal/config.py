import os
import sys
import shutil

class Config:
    def __init__(self):
        # 1. Detect Environment
        self.is_termux = "TERMUX_VERSION" in os.environ
        self.is_linux = sys.platform.startswith("linux") and not self.is_termux
        
        # 2. Check API Key
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("[ERROR] GEMINI_API_KEY environment variable is missing.")
            print("Please set it using: export GEMINI_API_KEY='your_key'")
            sys.exit(1)
            
        # 3. Validate System Dependencies
        self.validate_dependencies()

    def validate_dependencies(self):
        required_commands = ["mpv"] if not self.is_termux else ["termux-tts-speak"]
        for cmd in required_commands:
            if not shutil.which(cmd):
                print(f"[WARNING] Missing system dependency: '{cmd}'. Some voice functions may fail.")
