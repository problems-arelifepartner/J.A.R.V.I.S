import os
import subprocess
import tempfile
from typing import Optional

# Optional audio/input libraries
try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    from gtts import gTTS
except Exception:
    gTTS = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


class AudioEngine:
    def __init__(self, config):
        self.config = config
        # Only create a recognizer if SR is available
        if sr:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.dynamic_energy_threshold = True
            except Exception:
                self.recognizer = None
        else:
            self.recognizer = None

        # Initialize pyttsx3 engine lazily
        self._pytt_engine = None

    def display_logo(self):
        """Renders the J.A.R.V.I.S. logo directly in the terminal UI if term-image is available."""
        try:
            if os.path.exists(os.path.join(os.path.dirname(__file__), "1000216972.png")):
                try:
                    from term_image.image import from_file
                    logo = from_file(os.path.join(os.path.dirname(__file__), "1000216972.png"))
                    print(logo)
                except Exception:
                    # If term-image can't be used just skip quietly
                    pass
        except Exception:
            pass

    def _ensure_pyttsx3(self):
        if self._pytt_engine is not None:
            return True
        if not pyttsx3:
            return False
        try:
            self._pytt_engine = pyttsx3.init()
            return True
        except Exception:
            self._pytt_engine = None
            return False

    def speak(self, text: str):
        if not text or not text.strip():
            return

        # Print transcript to terminal for visibility
        try:
            print(f"\n🎙️ J.A.R.V.I.S.: {text}\n")
        except Exception:
            # Safe against weird console encodings
            print("J.A.R.V.I.S.:", text)

        # Termux TTS as highest-priority on Android
        try:
            if self.config.is_termux and shutil_which("termux-tts-speak"):
                subprocess.run(["termux-tts-speak", text], check=True)
                return
        except Exception:
            pass

        # Try offline TTS via pyttsx3 (local, no network)
        try:
            if self._ensure_pyttsx3():
                try:
                    self._pytt_engine.say(text)
                    self._pytt_engine.runAndWait()
                    return
                except Exception:
                    # If pyttsx3 fails, drop through to other options
                    pass
        except Exception:
            pass

        # Desktop fallback: gTTS -> mpv
        try:
            if gTTS:
                tts = gTTS(text=text, lang="en")
                # Use a temporary file for playback
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    temp_file = tmp.name
                try:
                    tts.save(temp_file)
                    # Try mpv playback if available
                    if shutil_which("mpv"):
                        subprocess.run(["mpv", "--no-video", "--really-quiet", temp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    else:
                        # As a fallback, try ffplay (part of ffmpeg)
                        if shutil_which("ffplay"):
                            subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", temp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                        else:
                            print("[Audio] mpv/ffplay not found; saved TTS to", temp_file)
                finally:
                    try:
                        os.remove(temp_file)
                    except Exception:
                        pass
                return
            else:
                print("[Audio] gTTS not installed; cannot perform desktop TTS.")
        except Exception as e:
            print(f"[Audio Output Error] Failed to speak via gTTS: {e}")

    def wait_for_wake_word(self, wake_word="jarvis"):
        if not self.recognizer:
            print("[Wake] speech_recognition is not installed; cannot perform local wake-word detection.")
            return False

        print(f"\n[Standby] Waiting for wake word: '{wake_word}'...")
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            except Exception:
                # Some systems may raise if microphone not accessible
                return False
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=4)
                    try:
                        text = self.recognizer.recognize_google(audio).lower()
                    except Exception:
                        continue
                    if wake_word in text:
                        return True
                except sr.WaitTimeoutError:
                    continue
                except Exception:
                    # Non-fatal — loop again
                    continue

    def listen(self, timeout=5, phrase_time_limit=10) -> str:
        if not self.recognizer:
            print("[Audio Input] speech_recognition not available.")
            return ""

        with sr.Microphone() as source:
            print("\n" + "=" * 50)
            self.display_logo()
            print("🔊 [AWAITING COMMAND]")
            print("=" * 50 + "\n")

            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            except Exception:
                pass
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Processing speech...")
                query = self.recognizer.recognize_google(audio)
                print(f"👤 You: {query}")
                return query
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"[Audio Input Error] {e}")
                return ""


# small cross-platform helper
def shutil_which(cmd: str) -> Optional[str]:
    try:
        import shutil
        return shutil.which(cmd)
    except Exception:
        return None
