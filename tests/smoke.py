"""
Smoke test to detect which AI backends are available and perform a dry run (no heavy API calls).
Run: python3 tests/smoke.py
"""
import os
from jarvis_terminal import genai_client as gc

print("=== Smoke Test ===")
print("OPENAI_API_KEY:", bool(os.environ.get('OPENAI_API_KEY')))
print("GEMINI_API_KEY:", bool(os.environ.get('GEMINI_API_KEY')))
print("LOCAL_MODE:", os.environ.get('LOCAL_MODE'))

print("python packages available:")
print(" - whisper:", 'whisper' in dir(gc) and gc.whisper is not None)
print(" - gpt4all:", 'gpt4all' in dir(gc) and gc.gpt4all is not None)
print(" - llama_cpp:", 'llama_cpp' in dir(gc) and gc.llama_cpp is not None)

print('\nTesting chat_response with small prompt...')
resp = gc.chat_response('Hello, this is a test. Say hello back in a single sentence.', system_instruction='You are a polite assistant.')
print('Response:', resp)
