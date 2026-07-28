#!/usr/bin/env python3
"""
Enhanced genai_client supporting three modes:
- Cloud: OpenAI (preferred) if OPENAI_API_KEY is set
- Cloud: Google Gemini if GEMINI_API_KEY is set
- Local: if LOCAL_MODE=1 or local model libraries are available (gpt4all/llama_cpp and whisper)

This file attempts to use python packages first (whisper, gpt4all, llama_cpp), then falls back to subprocess-based binaries if present.
"""
import os
import shutil
from typing import Optional

# Optional imports
try:
    import speech_recognition as sr
except Exception:
    sr = None

# Preferred cloud provider detection
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
LOCAL_MODE = os.environ.get("LOCAL_MODE") == "1"

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

# Local model python libs
whisper = None
try:
    import whisper as _whisper
    whisper = _whisper
except Exception:
    whisper = None

gpt4all = None
try:
    from gpt4all import GPT4All
    gpt4all = GPT4All
except Exception:
    gpt4all = None

llama_cpp = None
try:
    from llama_cpp import Llama
    llama_cpp = Llama
except Exception:
    llama_cpp = None

# Helpers
def _which(bin_name: str) -> Optional[str]:
    try:
        return shutil.which(bin_name)
    except Exception:
        return None

# Transcription
def transcribe_audio_local(path: str, prefer_whisper_tiny: bool = True) -> str:
    """Try multiple local transcription methods: whisper (python), SpeechRecognition, or binaries.
    Returns empty string on failure.
    """
    # 1) whisper python package: choose tiny model for low-RAM devices
    if whisper:
        try:
            model_name = os.environ.get("WHISPER_PY_MODEL") or ("tiny" if prefer_whisper_tiny else "small")
            model = whisper.load_model(model_name)
            result = model.transcribe(path)
            text = result.get("text", "")
            return text.strip()
        except Exception:
            pass

    # 2) speech_recognition fallback (uses Google web recognizer; requires network)
    if sr:
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(path) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text.strip()
        except Exception:
            pass

    # 3) whisper.cpp binary if present and model path provided
    whisper_bin = _which("main") or _which("whisper.cpp") or _which("whisper")
    whisper_model = os.environ.get("WHISPER_MODEL_PATH") or os.path.join("local_models", "whisper", "ggml-tiny.bin")
    if whisper_bin and os.path.exists(whisper_model):
        try:
            out = subprocess_check_output([whisper_bin, "-m", whisper_model, "-f", path])
            return out.strip()
        except Exception:
            pass

    return ""

# Chat / LLM
def chat_response(user_text: str, system_instruction: Optional[str] = None, max_tokens: int = 150) -> str:
    """Return a reply string. Tries cloud providers first, then local models if enabled.
    """
    if not user_text:
        return "I am sorry, I did not catch that."

    # 1) OpenAI
    if openai:
        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": user_text})
            # Try classic ChatCompletion
            try:
                resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens, temperature=0.6)
                return resp["choices"][0]["message"]["content"].strip()
            except Exception:
                # Try new client style (openai>=1.0 clients)
                try:
                    client = openai.OpenAI()
                    r = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens)
                    if hasattr(r, "choices"):
                        return r.choices[0].message.content
                    if isinstance(r, dict):
                        return r.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                except Exception:
                    pass
        except Exception:
            pass

    # 2) Gemini (google.generativeai)
    if genai:
        try:
            if hasattr(genai, "responses"):
                try:
                    resp = genai.responses.generate(model="gemini-3.5-pro", input=(system_instruction or "") + "\n\n" + user_text)
                    candidates = getattr(resp, "candidates", None)
                    if candidates and len(candidates) > 0:
                        c = candidates[0]
                        if hasattr(c, "content"):
                            return c.content.strip()
                        if isinstance(c, dict):
                            return c.get("content", "").strip()
                    if hasattr(resp, "output"):
                        return str(resp.output).strip()
                except Exception:
                    pass
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

    # 3) Local models if requested (LOCAL_MODE=1) or python libs present
    if LOCAL_MODE or gpt4all or llama_cpp:
        # Try GPT4All python package first
        if gpt4all:
            try:
                model_name = os.environ.get("GPT4ALL_MODEL_PATH") or os.path.join("local_models", "gpt4all", "gpt4all-model.bin")
                # Instantiate GPT4All model (lightweight settings recommended)
                mdl = gpt4all(model_name)
                prompt = (system_instruction + "\n\n" if system_instruction else "") + user_text
                resp = mdl.generate(prompt=prompt, max_tokens=max_tokens)
                if isinstance(resp, str):
                    return resp.strip()
                return str(resp).strip()
            except Exception:
                pass

        # Try llama_cpp
        if llama_cpp:
            try:
                model_path = os.environ.get("LLAMA_MODEL_PATH") or os.path.join("local_models", "llama", "model.bin")
                api = llama_cpp(model_path=str(model_path))
                prompt = (system_instruction + "\n\n" if system_instruction else "") + user_text
                r = api.create(prompt=prompt, max_tokens=max_tokens, temperature=0.6)
                if hasattr(r, "choices"):
                    return r.choices[0].text.strip()
                if isinstance(r, dict):
                    return r.get("choices", [{}])[0].get("text", "").strip()
            except Exception:
                pass

        # As last resort, try subprocess-based llama.cpp/gpt4all CLI if present
        if _which("gpt4all"):
            try:
                model_path = os.environ.get("GPT4ALL_MODEL_PATH") or os.path.join("local_models", "gpt4all", "gpt4all-model.bin")
                out = subprocess_check_output(["gpt4all", "-m", model_path, "-p", user_text])
                return out.strip()
            except Exception:
                pass

    # 4) Fallback: echo
    return f"I heard: {user_text}"

# Combined helper
def transcribe_and_chat(audio_path: str, system_instruction: Optional[str] = None) -> str:
    text = transcribe_audio_local(audio_path)
    if not text:
        return "Apologies, sir. I could not transcribe that audio."
    reply = chat_response(text, system_instruction=system_instruction)
    return reply

# small wrappers for subprocess
import subprocess

def subprocess_check_output(cmd_list):
    try:
        out = subprocess.check_output(cmd_list, stderr=subprocess.DEVNULL)
        if isinstance(out, bytes):
            return out.decode("utf-8", errors="ignore")
        return str(out)
    except Exception:
        return ""
