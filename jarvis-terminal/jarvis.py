#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import tempfile

from config import Config
from audio_engine import AudioEngine
import genai_client

# Try to import colorama, fallback
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RESET = Style.RESET_ALL
except Exception:
    GREEN = CYAN = RED = YELLOW = BLUE = RESET = ""

# Use safer temp file helpers
def safe_temp_filename(suffix=".aac"):
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tf.close()
    return tf.name

def clear_temp_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception:
            pass

def speak(engine: AudioEngine, text: str):
    try:
        engine.speak(text)
    except Exception:
        # fallback to printing
        print(text)

def verify_and_request_permissions(config: Config):
    """Checks and requests necessary permissions; returns True if ok."""
    print(f"{CYAN}[*] J.A.R.V.I.S. Core: Performing hardware & permission sweep...{RESET}")
    time.sleep(0.5)

    if config.is_termux:
        # Check termux tools existence
        if not shutil_which("termux-tts-speak") or not shutil_which("termux-microphone-record"):
            print(f"{RED}[!] PERMISSION/UTILITY WARNING: termux-api binaries are missing. Install 'termux-api' in Termux.{RESET}")
            return False

        # Try to run termux-setup-storage if storage not accessible
        storage_path = os.path.expanduser("~/storage")
        if not os.path.exists(storage_path):
            try:
                print(f"{YELLOW}[*] Initiating 'termux-setup-storage'...{RESET}")
                subprocess.run(["termux-setup-storage"], check=False)
                time.sleep(2)
            except Exception:
                pass

        # Microphone quick check (attempt short recording)
        test_file = safe_temp_filename(".aac")
        try:
            p = subprocess.Popen(["termux-microphone-record", "-f", test_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
            # stop
            subprocess.run(["termux-microphone-record", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(test_file) and os.path.getsize(test_file) > 0:
                clear_temp_file(test_file)
            else:
                print(f"{RED}[!] Microphone does not appear to be available.{RESET}")
                return False
        except Exception:
            print(f"{RED}[!] Microphone hardware check failed.{RESET}")
            return False
    else:
        # Desktop: ensure we have a recognizer if required
        # Not strictly requiring anything here; audio_engine will handle the lack of SR gracefully
        pass

    return True

def shutil_which(cmd: str):
    try:
        import shutil
        return shutil.which(cmd)
    except Exception:
        return None

def check_wake_word_via_transcription(audio_path, wake_words=None):
    # Transcribe using genai_client's local transcription
    text = genai_client.transcribe_audio_local(audio_path)
    return genai_client.detect_wake_word_from_text(text, wake_words=wake_words)

def capture_and_process_command(engine: AudioEngine, system_instruction: str):
    """Records audio and uses genai_client to transcribe & respond."""
    cmd_file = safe_temp_filename(".wav")
    try:
        # Termux recording preferred when available
        if engine.config.is_termux and shutil_which("termux-microphone-record"):
            # start recording, stop after fixed duration
            p = subprocess.Popen(["termux-microphone-record", "-f", cmd_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(5.5)
            try:
                subprocess.run(["termux-microphone-record", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
        else:
            # Non-termux: try arecord or fallback to speech_recognition usage (we will instruct user to run via audio_engine.listen)
            # For simplicity, call audio_engine.listen() to get a transcription directly
            transcription = engine.listen()
            if not transcription:
                speak(engine, "I am sorry, sir. I did not detect any input. Returning to standby.")
                return
            # Ask LLM for a response
            reply = genai_client.chat_response(transcription, system_instruction=system_instruction)
            speak(engine, reply)
            return

        # If file exists and seems valid, use genai_client to transcribe & chat
        if not os.path.exists(cmd_file) or os.path.getsize(cmd_file) == 0:
            speak(engine, "I am sorry, sir. I did not detect any input. Returning to standby.")
            clear_temp_file(cmd_file)
            return

        # Use wrapper to transcribe and reply
        reply = genai_client.transcribe_and_chat(cmd_file, system_instruction=system_instruction)
        speak(engine, reply)
    except Exception as e:
        print(f"{RED}[!] Command processing failed: {e}{RESET}")
        speak(engine, "Apologies, sir. The mainframe encountered an interface error processing that request.")
    finally:
        clear_temp_file(cmd_file)

def main():
    config = Config()
    config.show_warnings()

    # Verify permissions (best-effort)
    ok = verify_and_request_permissions(config)
    if not ok:
        print(f"{RED}[!] Permissions / dependencies not satisfied. Exiting.{RESET}")
        sys.exit(1)

    # Startup UI
    engine = AudioEngine(config)
    print(f"{BLUE}==================================================")
    print(f"{BLUE}         STARK INDUSTRIES MAINFRAME              ")
    print(f"{BLUE}               SYSTEM VERSION 12.0.0             ")
    print(f"{BLUE}=================================================={RESET}")
    time.sleep(0.3)
    engine.display_logo()
    time.sleep(0.3)

    # Load API key from config if available and configure genai_client if needed
    if config.has_api_key():
        # prefer OpenAI env var already enforced by genai_client import
        pass
    else:
        print(f"{YELLOW}[*] Warning: No API key detected. The assistant will still try local transcription and fallbacks.{RESET}")

    # System instructions for persona
    system_instruction = (
        "You are J.A.R.V.I.S., a polite, intelligent British assistant. "
        "Address the user as 'Sir' or 'Ma'am'. Keep replies natural and voice-friendly."
    )

    # Standby loop: passive wake detection via short recordings if termux, otherwise rely on audio_engine.listen
    try:
        print(f"{GREEN}[+] Mainframe linked. Standby acoustic monitoring active.{RESET}")
        speak(engine, "Uplink established, sir. Mainframe is in standby. Speak the activation phrase when ready.")
    except Exception:
        pass

    try:
        while True:
            try:
                if config.is_termux and shutil_which("termux-microphone-record"):
                    # Create a short audio snippet and try to detect wake-word via local transcription
                    wake_file = safe_temp_filename(".wav")
                    try:
                        p = subprocess.Popen(["termux-microphone-record", "-f", wake_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(2.5)
                        try:
                            subprocess.run(["termux-microphone-record", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        except Exception:
                            pass

                        if os.path.exists(wake_file) and os.path.getsize(wake_file) > 0:
                            triggered = check_wake_word_via_transcription(wake_file)
                        else:
                            triggered = False
                    finally:
                        clear_temp_file(wake_file)

                    if triggered:
                        print(f"\n{GREEN}[✓] Trigger Word Detected. Activating Command Mainframe...{RESET}")
                        speak(engine, "Always, sir. What is your directive?")
                        capture_and_process_command(engine, system_instruction)
                else:
                    # Non-termux: use local wake detection via the recognizer (blocking; user must say wake word)
                    if engine.recognizer:
                        triggered = engine.wait_for_wake_word()
                        if triggered:
                            print(f"\n{GREEN}[✓] Trigger Word Detected. Activating Command Mainframe...{RESET}")
                            speak(engine, "Always, sir. What is your directive?")
                            capture_and_process_command(engine, system_instruction)
                    else:
                        # no recognizer available: fallback sleep until user manually triggers by pressing Enter
                        print("[Info] No microphone/recognizer available. Press Enter to simulate activation, or Ctrl+C to quit.")
                        input()
                        capture_and_process_command(engine, system_instruction)
                # small sleep to avoid busy loop
                time.sleep(0.2)
            except KeyboardInterrupt:
                print(f"\n\n{GREEN}J.A.R.V.I.S: Mainframe disconnected. Goodbye, sir.{RESET}")
                speak(engine, "Mainframe disconnected. Goodbye, sir.")
                break
            except Exception as e:
                # Log and continue loop
                print(f"{RED}[Loop Error] {e}{RESET}")
                time.sleep(1)
    finally:
        pass

if __name__ == "__main__":
    main()
