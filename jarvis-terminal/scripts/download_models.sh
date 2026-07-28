#!/usr/bin/env bash
set -e

# Automatic lightweight model downloader for low-RAM mobile (4GB) and desktop.
# This script attempts to download small/quantized models suitable for devices with ~4GB RAM.
# It will only download if DOWNLOAD_MODELS=1 is set in environment to avoid unexpected large downloads.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_MODELS_DIR="$ROOT_DIR/local_models"
WHISPER_DIR="$LOCAL_MODELS_DIR/whisper"
GPT4ALL_DIR="$LOCAL_MODELS_DIR/gpt4all"
LLAMA_DIR="$LOCAL_MODELS_DIR/llama"

mkdir -p "$WHISPER_DIR" "$GPT4ALL_DIR" "$LLAMA_DIR"

echo "Local models directory: $LOCAL_MODELS_DIR"

if [ "${DOWNLOAD_MODELS}" != "1" ]; then
  echo "DOWNLOAD_MODELS is not set to 1; skipping automatic downloads."
  echo "To enable automatic download set: export DOWNLOAD_MODELS=1 and rerun this script."
  exit 0
fi

# Default small model URLs - these are suggestions and may change. If a URL fails, set an environment variable to override.
WHISPER_URL=${WHISPER_URL:-"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/models/ggml-tiny.bin"}
GPT4ALL_URL=${GPT4ALL_URL:-"https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin"}
LLAMA_URL=${LLAMA_URL:-""}

# Download helper
fetch_file() {
  url="$1"
  dest="$2"
  if [ -z "$url" ]; then
    echo "No URL provided for $dest"
    return 1
  fi
  if [ -f "$dest" ]; then
    echo "$dest already exists, skipping."
    return 0
  fi
  echo "Downloading $url -> $dest"
  if command -v curl >/dev/null 2>&1; then
    curl -L --fail --progress-bar -o "$dest" "$url" || return 1
  elif command -v wget >/dev/null 2>&1; then
    wget -O "$dest" "$url" || return 1
  else
    echo "curl or wget required to download files."; return 1
  fi
  echo "Downloaded $dest"
}

# Whisper tiny model (smallest reasonably accurate)
WHISPER_DEST="$WHISPER_DIR/ggml-tiny.bin"
if fetch_file "$WHISPER_URL" "$WHISPER_DEST"; then
  echo "Whisper model ready: $WHISPER_DEST"
else
  echo "Failed to fetch whisper tiny model. You can set WHISPER_URL env var to a different URL and retry."
fi

# GPT4All (suggested small/compatible model)
GPT4ALL_DEST="$GPT4ALL_DIR/gpt4all-model.bin"
if [ -n "$GPT4ALL_URL" ]; then
  if fetch_file "$GPT4ALL_URL" "$GPT4ALL_DEST"; then
    echo "GPT4All model ready: $GPT4ALL_DEST"
  else
    echo "Failed to fetch GPT4All model. You can set GPT4ALL_URL env var to a different URL and retry."
  fi
else
  echo "No GPT4ALL_URL configured; skip GPT4All model download."
fi

# LLAMA: left blank by default due to many variants and licensing
if [ -n "$LLAMA_URL" ]; then
  LLAMA_DEST="$LLAMA_DIR/llama-model.bin"
  if fetch_file "$LLAMA_URL" "$LLAMA_DEST"; then
    echo "LLAMA model ready: $LLAMA_DEST"
  else
    echo "Failed to fetch LLAMA model. You can set LLAMA_URL env var to a different URL and retry."
  fi
else
  echo "No LLAMA_URL configured; skipping llama downloads by default."
fi

echo "Download script finished. Verify models in $LOCAL_MODELS_DIR and set environment variables:
 - WHISPER_MODEL_PATH=$WHISPER_DEST
 - GPT4ALL_MODEL_PATH=$GPT4ALL_DEST
 - LLAMA_MODEL_PATH=..."
