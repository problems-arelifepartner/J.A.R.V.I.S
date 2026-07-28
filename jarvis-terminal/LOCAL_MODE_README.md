# Local mode setup instructions and helpers

This script prints instructions for setting up local models (Whisper for transcription and GPT4All/llama.cpp for chat).

Place model files under local_models/whisper/ and local_models/llama/ or set environment variables:
- WHISPER_MODEL_PATH -> path to whisper model (optional, only for whisper python)
- GPT4ALL_MODEL_PATH -> path to gpt4all model binary
- LLAMA_MODEL_PATH -> path to llama ggml model

Example notes:
- For whisper (python): pip install -U openai-whisper and download a model via whisper.load_model('small') (the library will fetch it).
- For GPT4All: follow https://gpt4all.io/ to download a model; set GPT4ALL_MODEL_PATH to the downloaded .bin file.
- For llama.cpp / llama_cpp python: build llama.cpp and download a ggml model; set LLAMA_MODEL_PATH to the model path.

This repository cannot host model weights; you must download them yourself due to licensing.
