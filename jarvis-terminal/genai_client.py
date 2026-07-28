@@
 def transcribe_audio_local(path: str, prefer_whisper_tiny: bool = True) -> str:
@@
     return ""
+
+
+def detect_wake_word_from_text(text: str, wake_words=None) -> bool:
+    if not text:
+        return False
+    if wake_words is None:
+        wake_words = ["hey jarvis", "hay jarvis", "jarvis", "wake up buddy", "hay buddy", "hey buddy", "assemble", "virtual mouse", "open virtual mouse", "mouse mode", "start virtual mouse"]
+    text_low = text.lower()
+    return any(w in text_low for w in wake_words)
@@
 def subprocess_check_output(cmd_list):
@@
     except Exception:
         return ""
