*** Begin Patch
*** Update File: jarvis-terminal/jarvis.py
@@
-def main():
+def main():
@@
-    try:
-        print(f"{GREEN}[+] Mainframe linked. Standby acoustic monitoring active.{RESET}")
-        speak(engine, "Uplink established, sir. Mainframe is in standby. Speak the activation phrase when ready.")
-    except Exception:
-        pass
+    try:
+        print(f"{GREEN}[+] Mainframe linked. Standby acoustic monitoring active.{RESET}")
+        speak(engine, "Uplink established, sir. Mainframe is in standby. Speak the activation phrase when ready.")
+    except Exception as e:
+        # Log and continue; don't allow UI speak failure to break startup
+        print(f"[Startup Warning] Failed to play TTS: {e}")
@@
-            try:
+            try:
                 if config.is_termux and shutil_which("termux-microphone-record"):
@@
-                    if triggered:
-                        print(f"\n{GREEN}[✓] Trigger Word Detected. Activating Command Mainframe...{RESET}")
-                        speak(engine, "Always, sir. What is your directive?")
-                        capture_and_process_command(engine, system_instruction)
+                    if triggered:
+                        print(f"\n{GREEN}[✓] Trigger Word Detected. Activating Command Mainframe...{RESET}")
+                        try:
+                            speak(engine, "Always, sir. What is your directive?")
+                        except Exception:
+                            pass
+                        capture_and_process_command(engine, system_instruction)
@@
-                    if engine.recognizer:
-                        triggered = engine.wait_for_wake_word()
-                        if triggered:
-                            print(f"\n{GREEN}[✓] Trigger Word Detected. Activating Command Mainframe...{RESET}")
-                            speak(engine, "Always, sir. What is your directive?")
-                            capture_and_process_command(engine, system_instruction)
+                    if engine.recognizer:
+                        try:
+                            triggered = engine.wait_for_wake_word()
+                        except Exception:
+                            triggered = False
+                        if triggered:
+                            print(f"\n{GREEN}[✓] Trigger Word Detected. Activating Command Mainframe...{RESET}")
+                            try:
+                                speak(engine, "Always, sir. What is your directive?")
+                            except Exception:
+                                pass
+                            capture_and_process_command(engine, system_instruction)
*** End Patch
