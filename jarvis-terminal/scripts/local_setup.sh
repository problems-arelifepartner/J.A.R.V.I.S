#!/usr/bin/env bash
set -e

echo "This script will check for common local model python libs and binaries and offer guidance."

command -v python3 >/dev/null 2>&1 || { echo "python3 not found; please install Python 3"; exit 1; }

echo "Checking Python packages..."
python3 - <<'PY'
import importlib
for pkg in ['whisper','gpt4all','llama_cpp','speech_recognition']:
    try:
        importlib.import_module(pkg)
        print(pkg + ' : OK')
    except Exception:
        print(pkg + ' : MISSING')
PY

cat <<'EOS'

If you want fully-local free operation, install the Python packages above and download model weights:
- whisper (python) -> pip install -U openai-whisper
  then in Python: import whisper; model = whisper.load_model('small') # will download
- gpt4all -> follow https://gpt4all.io/ to download a model and install the gpt4all package
- llama_cpp -> use llama.cpp or llama-cpp-python with a ggml model

Model files should be placed under local_models/ (see LOCAL_MODE_README.md for variable names).
EOS
