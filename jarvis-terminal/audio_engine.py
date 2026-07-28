import os
import subprocess
import tempfile
from typing import Optional

try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    from gtts import gTTS
except Exception:
    gTTS = None

class AudioEngine:
    def __init__(self, config):
        self.config = config
        # Only create a recognizer if SR is available
        if sr:
            self.recognizer = sr.Recognizer()
            self.recognizer.dynamic_energy_threshold = True
        else:
            self.recognizer = None

    def display_logo(self):
        """Renders the J.A.R.V.I.S. logo directly in the terminal UI if term-image is available."""
        try:
            if os.path.exists("1000216972.png"):
                try:
                    from term_image.image import from_file
                    logo = from_file("1000216972.png")
                    print(logo)
                except Exception:
                    # If term-image can't be used just skip quietly
                    pass
        except Exception:
            pass

    def speak(self, text: str):
        if not text or not text.strip():
            return

        print(f"\n🎙️ J.A.R.V.I.S.: {text}\n")

        try:
            if self.config.is_termux and shutil_which("termux-tts-speak"):
                # prefer termux TTS when available
                subprocess.run(["termux-tts-speak", text], check=True)
                return
        except Exception:
            pass

        # Desktop fallback: gTTS -> mpv
        try:
            if gTTS:
                tts = gTTS(text=text, lang="en")
                # Use a temporary file for playback
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    temp_file = tmp.name
                tts.save(temp_file)
                # Try mpv playback if available
                if shutil_which("mpv"):
                    subprocess.run(["mpv", "--no-video", "--really-quiet", temp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                else:
                    # As a fallback, try ffplay (part of ffmpeg) or simply print text
                    print("[Audio] mpv not found; saved TTS to", temp_file)
                try:
                    os.remove(temp_file)
                except Exception:
                    pass
            else:
                print("[Audio] gTTS not installed; cannot perform desktop TTS.")
        except Exception as e:
            print(f"[Audio Output Error] Failed to speak: {e}")

    def wait_for_wake_word(self, wake_word="jarvis"):
        if not self.recognizer:
            print("[Wake] speech_recognition is not installed; cannot perform local wake-word detection.")
            return False

        print(f"\n[Standby] Waiting for wake word: '{wake_word}'...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    if wake_word in text:
                        return True
                except sr.UnknownValueError:
                    pass
                except sr.WaitTimeoutError:
                    continue
                except Exception:
                    # Non-fatal — loop again
                    pass

    def listen(self, timeout=5, phrase_time_limit=10) -> str:
        if not self.recognizer:
            print("[Audio Input] speech_recognition not available.")
            return ""

        with sr.Microphone() as source:
            print("\n" + "="*50)
            self.display_logo()
            print("🔊 [AWAITING COMMAND]")
            print("="*50 + "\n")

            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
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
