"""Lightweight GenAI client helpers used by jarvis-terminal.

This module provides minimal, dependency-tolerant functions that other parts
of the project expect. It intentionally avoids making network calls unless
an API key is available and the relevant libraries are installed.
"""

import os
import subprocess
from typing import List

# Optional imports
try:
    import whisper
except Exception:
    whisper = None

try:
    import gpt4all
except Exception:
    gpt4all = None

try:
    import openai
except Exception:
    openai = None


def transcribe_audio_local(path: str, prefer_whisper_tiny: bool = True) -> str:
    """Attempt to transcribe an audio file using whisper if available.
    Returns an empty string on failure.
    """
    if not whisper:
        return ""
    try:
        model_name = "tiny" if prefer_whisper_tiny else "small"
        model = whisper.load_model(model_name)
        result = model.transcribe(path)
        return result.get("text", "")
    except Exception:
        return ""


def chat_response(prompt: str, system_instruction: str = "You are a helpful assistant.") -> str:
    """Return a lightweight chat response. Prefer local gpt4all if available, then OpenAI/GPT
    only if API key and package available. Falls back to echoing the prompt.
    """
    # gpt4all local model (if installed)
    try:
        if gpt4all:
            try:
                m = gpt4all.GPT4All()
                return m.generate(prompt)
            except Exception:
                # ignore and fall through
                pass

        # OpenAI (if key + package available)
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if api_key and openai:
            try:
                openai.api_key = api_key
                # Use a minimal completion call to reduce dependency complexity
                resp = openai.Completion.create(engine="text-davinci-003", prompt=system_instruction + "\n" + prompt, max_tokens=150)
                choices = resp.get("choices")
                if choices:
                    return choices[0].get("text", "").strip()
            except Exception:
                pass
    except Exception:
        pass

    # No model available — return a polite echo fallback
    return f"I heard: {prompt}"


def detect_wake_word_from_text(text: str, wake_words=None) -> bool:
    """Return True if text contains any wake word.
    This is a small utility used by the voice loop.
    """
    if not text:
        return False
    if wake_words is None:
        wake_words = [
            "hey jarvis",
            "hay jarvis",
            "jarvis",
            "wake up buddy",
            "hay buddy",
            "hey buddy",
            "assemble",
            "virtual mouse",
            "open virtual mouse",
            "mouse mode",
            "start virtual mouse",
        ]
    text_low = text.lower()
    return any(w in text_low for w in wake_words)


def subprocess_check_output(cmd_list: List[str]) -> str:
    """Run a subprocess and return its stdout as text, or empty string on error."""
    try:
        out = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT, text=True)
        return out
    except Exception:
        return ""
