import os
import subprocess
import speech_recognition as sr
from gtts import gTTS

class AudioEngine:
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        # Adjust dynamics for background noise filtering
        self.recognizer.dynamic_energy_threshold = True

    def speak(self, text: str):
        """Outputs text into voice format based on the OS platform."""
        if not text.strip():
            return

        print(f"\n🎙️ J.A.R.V.I.S.: {text}")
        
        try:
            if self.config.is_termux:
                # Use Android's native ultra-fast text-to-speech engine via Termux-API
                subprocess.run(["termux-tts-speak", text], check=True)
            else:
                # Linux fallback: Generate high-quality gTTS audio stream and play via mpv cleanly
                tts = gTTS(text=text, lang="en", tld="co.uk")  # British accent profile
                temp_file = "/tmp/jarvis_resp.mp3"
                tts.save(temp_file)
                subprocess.run(["mpv", "--no-video", "--volume=100", temp_file], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        except Exception as e:
            print(f"[Audio Output Error] Failed to speak: {e}")

    def wait_for_wake_word(self, wake_word="jarvis"):
        """Lightweight background loop waiting for the wake word."""
        print(f"\n[Standby] Waiting for wake word: '{wake_word}'...")
        
        with sr.Microphone() as source:
            # Adjust for background noise once before entering the loop
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while True:
                try:
                    # Listen in very short 3-second windows to save memory and processing
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    # --- WAKE WORD ENGINE ---
                    # Default: Google Web API (Requires internet, might hit rate limits if left on 24/7)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    # PRO-TIP: If you install pocketsphinx (pip install pocketsphinx), 
                    # comment out the Google line above and uncomment the line below for offline listening:
                    # text = self.recognizer.recognize_sphinx(audio).lower()
                    
                    if wake_word in text:
                        print("\n[Wake Word Detected!]")
                        return True
                        
                except sr.UnknownValueError:
                    # Normal behavior: background noise was heard but wasn't understood. Ignore.
                    pass 
                except sr.WaitTimeoutError:
                    # Normal behavior: no one spoke during the timeout window. Loop silently.
                    continue
                except Exception as e:
                    # Suppress minor connection drops to keep the loop alive
                    pass

    def listen(self) -> str:
        """Captures active command audio from microphone cleanly and returns text."""
        with sr.Microphone() as source:
            print("Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                # Using Google's web speech API for high-accuracy complex command parsing
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
