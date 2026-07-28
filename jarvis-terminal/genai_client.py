"""
Robust AI client wrapper that supports OpenAI (preferred) and Google Generative AI (Gemini) as a fallback.
This file attempts multiple call patterns to accommodate differences between SDK versions.
"""
import os
from typing import Optional

# Optional imports
try:
    import speech_recognition as sr
except Exception:
    sr = None

# Detect keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or None

openai = None
if OPENAI_API_KEY:
    try:
        import openai as _openai
        _openai.api_key = OPENAI_API_KEY
        openai = _openai
    except Exception:
        openai = None

# Google generative ai (gemini)
genai = None
if GEMINI_API_KEY:
    try:
        import google.generativeai as _genai
        _genai.configure(api_key=GEMINI_API_KEY)
        genai = _genai
    except Exception:
        genai = None


def transcribe_audio_local(path: str) -> str:
    """Transcribe audio using OpenAI Whisper (if available) or SpeechRecognition fallback."""
    # 1) try OpenAI Whisper transcription if openai client available
    if openai and hasattr(openai, "Audio"):
        try:
            with open(path, "rb") as af:
                # many openai sdk versions expose openai.Audio.transcribe
                if hasattr(openai, "Audio") and hasattr(openai.Audio, "transcribe"):
                    resp = openai.Audio.transcribe("whisper-1", af)
                    # resp may be a dict or object; try to extract text
                    if isinstance(resp, dict):
                        return resp.get("text", "").strip()
                    if hasattr(resp, "text"):
                        return resp.text.strip()
        except Exception:
            pass
    # 2) try SpeechRecognition local transcription
    if sr:
        try:
            r = sr.Recognizer()
            with sr.AudioFile(path) as source:
                audio = r.record(source)
            text = r.recognize_google(audio)
            return text.strip()
        except Exception:
            return ""
    return ""


def detect_wake_word_from_text(text: str, wake_words=None) -> bool:
    if not text:
        return False
    if wake_words is None:
        wake_words = ["hey jarvis", "hay jarvis", "jarvis", "wake up buddy", "hay buddy", "hey buddy", "assemble"]
    text_low = text.lower()
    return any(w in text_low for w in wake_words)


def chat_response(user_text: str, system_instruction: Optional[str] = None, max_tokens: int = 512) -> str:
    """Return a reply string. Try OpenAI, then Google Generative AI, else fallback."""
    if not user_text:
        return "I am sorry, I did not catch that."

    # 1) OpenAI ChatCompletion (classic)
    if openai:
        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": user_text})
            # Try older ChatCompletion API
            resp = None
            try:
                resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens, temperature=0.6)
                return resp["choices"][0]["message"]["content"].strip()
            except Exception:
                # Try newer patterns (openai.Chat.create or client-based)
                try:
                    client = openai.OpenAI()
                    r = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens)
                    # response structure may differ
                    if hasattr(r, "choices"):
                        return r.choices[0].message.content
                    if isinstance(r, dict):
                        return r.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                except Exception:
                    pass
        except Exception:
            pass

    # 2) Google Generative AI (Gemini) via google.generativeai (best-effort)
    if genai:
        try:
            # Preferred new-style responses API
            if hasattr(genai, "responses"):
                try:
                    resp = genai.responses.generate(model="gemini-3.5-pro", input=(system_instruction or "") + "\n\n" + user_text)
                    # extract text from response
                    if hasattr(resp, "candidates") and len(resp.candidates) > 0:
                        c = resp.candidates[0]
                        if hasattr(c, "content"):
                            return c.content.strip()
                        if isinstance(c, dict):
                            return c.get("content", "").strip()
                    # fallback to resp.output
                    if hasattr(resp, "output"):
                        return str(resp.output).strip()
                except Exception:
                    pass
            # older helper
            if hasattr(genai, "generate_text"):
                try:
                    resp = genai.generate_text(model="gemini-3.5-pro", prompt=(system_instruction or "") + "\n\n" + user_text)
                    if hasattr(resp, "text"):
                        return resp.text.strip()
                    if isinstance(resp, dict):
                        return resp.get("candidates", [{}])[0].get("content", "").strip()
                except Exception:
                    pass
        except Exception:
            pass

    # 3) fallback
    return f"I heard: {user_text}"


def transcribe_and_chat(audio_path: str, system_instruction: Optional[str] = None) -> str:
    # Try to transcribe using best available method
    text = transcribe_audio_local(audio_path)
    if not text:
        return "Apologies, sir. I could not transcribe that audio."
    # Then chat
    reply = chat_response(text, system_instruction=system_instruction)
    return reply
