import os
import sys

class Config:
    def __init__(self):
        # Detect environment
        self.is_termux = "TERMUX_VERSION" in os.environ
        self.is_linux = sys.platform.startswith("linux") and not self.is_termux

        # API keys: prefer environment variables, then api_key.txt
        self.api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or self._load_api_key_file()

        # Validate system dependencies (log warnings, but don't exit — higher-level code will decide)
        self.missing_commands = []
        self.validate_dependencies()

    def _load_api_key_file(self):
        """Reads the user's API key from the local file if present, otherwise return None."""
        try:
            if os.path.exists("api_key.txt"):
                with open("api_key.txt", "r") as f:
                    key = f.read().strip()
                    return key or None
        except Exception:
            pass
        return None

    def validate_dependencies(self):
        # Termux: expect termux-tts-speak; Desktop: mpv for playback (used by audio_engine)
        try:
            import shutil
            required_commands = ["termux-tts-speak"] if self.is_termux else ["mpv"]
            for cmd in required_commands:
                if not shutil.which(cmd):
                    self.missing_commands.append(cmd)
        except Exception:
            # If shutil isn't available for some reason, don't crash here
            pass

    def has_api_key(self):
        return bool(self.api_key)

    def show_warnings(self):
        if self.missing_commands:
            print("[WARNING] Missing system commands:", ", ".join(self.missing_commands))
            if self.is_termux:
                print("[WARNING] Install termux-api package in Termux (pkg install termux-api).")
            else:
                print("[WARNING] Install mpv (sudo apt install mpv) for desktop audio playback.")
        if not self.api_key:
            print("[WARNING] No API key detected. Please set OPENAI_API_KEY or GEMINI_API_KEY env var or write a key into api_key.txt.")
