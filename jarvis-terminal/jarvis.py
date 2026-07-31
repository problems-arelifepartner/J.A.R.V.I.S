"""Main terminal launcher for J.A.R.V.I.S.

This file provides a robust, dependency-tolerant main loop that uses the
available audio/audio-engine support when installed, and falls back to a
text-based REPL otherwise. It intentionally avoids hard failures when
optional packages are missing and aims to be ready-to-run on a plain
Python environment.

Commands supported (voice or text):
 - exit|quit                    -> stop the assistant
 - list [dir]                   -> list files in directory (default .)
 - read <path>                  -> print start of a file
 - run <shell command>          -> execute a limited shell command
 - open virtual mouse|virtual mouse -> attempt to start the virtual mouse helper
Any other input is echoed back using a simple chat_response fallback.
"""

import sys
import os
import subprocess
import threading
import time

from config import Config
from audio_engine import AudioEngine
import tools
import genai_client as gc

# Colors (best-effort)
try:
    from colorama import init as _cinit, Fore, Style
    _cinit()
    GREEN = Fore.GREEN
    RESET = Style.RESET_ALL
except Exception:
    GREEN = ""
    RESET = ""


def process_command(text: str, engine: AudioEngine, cfg: Config) -> bool:
    """Process a single command string. Returns True to continue, False to exit."""
    if not text:
        engine.speak("I didn't catch that. Try again or type a command.")
        return True

    cmd = text.strip()
    low = cmd.lower()

    # exit
    if any(w in low for w in ("exit", "quit", "goodbye", "shutdown")):
        engine.speak("Shutting down. Goodbye.")
        return False

    # list files
    if low.startswith("list") or low == "ls":
        parts = cmd.split(maxsplit=1)
        directory = parts[1] if len(parts) > 1 else "."
        res = tools.list_files(directory)
        if res.get("status") == "success":
            engine.speak(f"Listing files in {res.get('directory')}.")
            for item in res.get("contents", [])[:200]:
                print(item)
        else:
            engine.speak("Failed to list files: " + res.get("message", "unknown"))
        return True

    # read file
    if low.startswith("read ") or low.startswith("open file"):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            engine.speak("Please tell me the file path to read.")
            return True
        path = parts[1].strip()
        res = tools.read_file_content(path)
        if res.get("status") == "success":
            engine.speak(f"Contents of {res.get('filepath')}:")
            print(res.get("content"))
        else:
            engine.speak("Could not read file: " + res.get("message", "unknown"))
        return True

    # run shell command
    if low.startswith("run ") or low.startswith("execute "):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            engine.speak("Please provide a command to run.")
            return True
        command = parts[1]
        res = tools.execute_system_command(command)
        if res.get("status") == "success":
            out = res.get("stdout") or "(no stdout)"
            err = res.get("stderr") or ""
            print("STDOUT:\n", out)
            if err:
                print("STDERR:\n", err)
            engine.speak("Command completed. Check terminal output.")
        else:
            engine.speak("Command failed: " + res.get("message", "unknown"))
        return True

    # virtual mouse
    if "virtual mouse" in low or "open virtual mouse" in low or "start virtual mouse" in low:
        # try to run the packaged virtual mouse script in a new process
        vm_path = os.path.join(os.path.dirname(__file__), "virtual_mouse", "main.py")
        if os.path.exists(vm_path):
            try:
                subprocess.Popen([sys.executable, vm_path])
                engine.speak("Virtual mouse launched.")
            except Exception as e:
                engine.speak("Failed to start virtual mouse: " + str(e))
        else:
            engine.speak("Virtual mouse component not found.")
        return True

    # fallback: use simple chat_response (non-blocking and lightweight)
    try:
        resp = gc.chat_response(cmd, system_instruction="You are a helpful assistant.")
    except Exception as e:
        resp = f"(chat fallback failed: {e}) I heard: {cmd}"

    engine.speak(resp)
    return True


def text_repl(engine: AudioEngine, cfg: Config):
    engine.speak("Text mode active. Type 'exit' to quit.")
    while True:
        try:
            inp = input("J.A.R.V.I.S> ")
        except (EOFError, KeyboardInterrupt):
            print()
            engine.speak("Goodbye.")
            break
        cont = process_command(inp, engine, cfg)
        if not cont:
            break


def voice_loop(engine: AudioEngine, cfg: Config):
    engine.speak("Voice mode active. Say the wake word to give a command.")
    while True:
        try:
            triggered = False
            try:
                triggered = engine.wait_for_wake_word()
            except Exception:
                # give up on fancy wake-word detection and fall back to listening for a single utterance
                triggered = False

            if not triggered:
                # allow typed activation if audio is unavailable
                print("(no wake word detected) Type 's' then Enter to speak or 'q' to quit")
                val = input("[s=listen/q=quit/enter=skip]>")
                if val.strip().lower() == "q":
                    engine.speak("Goodbye.")
                    break
                if val.strip().lower() != "s":
                    continue

            engine.speak("Listening for your command.")
            cmd = engine.listen()
            if not cmd:
                engine.speak("I didn't hear anything.")
                continue
            # If the user spoke a wake-word plus command, strip wake words if present
            if gc.detect_wake_word_from_text(cmd):
                # naive: remove the first occurrence of a wake word phrase
                for w in ["hey jarvis", "jarvis", "wake up buddy", "hey buddy", "start virtual mouse"]:
                    if w in cmd.lower():
                        cmd = cmd.lower().replace(w, "").strip()
                        break

            cont = process_command(cmd, engine, cfg)
            if not cont:
                break

        except (KeyboardInterrupt, EOFError):
            engine.speak("Goodbye.")
            break
        except Exception as e:
            # write traceback to log file for user debugging
            import traceback
            tb = traceback.format_exc()
            with open("jarvis-terminal/jarvis_error.log", "w") as f:
                f.write(tb)
            print("An unexpected error occurred. See jarvis-terminal/jarvis_error.log")
            engine.speak("An error occurred; check jarvis_error.log for details.")
            break


def main():
    cfg = Config()
    cfg.show_warnings()

    engine = AudioEngine(cfg)

    # Friendly startup message
    print(f"{GREEN}[+] J.A.R.V.I.S. starting up...{RESET}")
    try:
        engine.speak("Uplink established. Awaiting your command.")
    except Exception as e:
        print("[Startup Warning] speak failed:", e)

    # Choose mode depending on audio availability
    if engine.recognizer:
        voice_loop(engine, cfg)
    else:
        text_repl(engine, cfg)


if __name__ == "__main__":
    sys.exit(main())
