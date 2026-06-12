import os
import subprocess
import speech_recognition as sr
from gtts import gTTS

class AudioEngine:
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True

    def display_logo(self):
        """Renders the J.A.R.V.I.S. logo directly in the terminal ui."""
        try:
            if os.path.exists("1000216972.png"):
                from term_image.image import from_file
                logo = from_file("1000216972.[span_2](start_span)png")
                # Calling print on the image object automatically draws it in the terminal[span_2](end_span)
                print(logo)
        except Exception as e:
            # Silently pass if the terminal scale is too small or image fails to render
            pass

    def speak(self, text: str):
        if not text.strip():
            return

        print(f"\n🎙️ J.A.R.V.I.S.: {text}")
        
        try:
            if self.config.is_termux:
                subprocess.run(["termux-tts-speak", text], check=True)
            else:
                tts = gTTS(text=text, lang="en", tld="co.uk")
                temp_file = "/tmp/jarvis_resp.mp3"
                tts.save(temp_file)
                subprocess.run(["mpv", "--no-video", "--volume=100", temp_file], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        except Exception as e:
            print(f"[Audio Output Error] Failed to speak: {e}")

    def wait_for_wake_word(self, wake_word="jarvis"):
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
                    pass

    def listen(self) -> str:
        with sr.Microphone() as source:
            # --- VISUAL UI TRIGGER ---
            print("\n" + "="*50)
            self.display_logo()
            print("🔊 [AWAITING COMMAND]")
            print("="*50 + "\n")
            
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
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
