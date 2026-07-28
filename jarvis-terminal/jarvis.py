@@
 def capture_and_process_command(engine: AudioEngine, system_instruction: str):
@@
-        if not os.path.exists(cmd_file) or os.path.getsize(cmd_file) == 0:
+        if not os.path.exists(cmd_file) or os.path.getsize(cmd_file) == 0:
             speak(engine, "I am sorry, sir. I did not detect any input. Returning to standby.")
             clear_temp_file(cmd_file)
             return
-
-        # Use wrapper to transcribe and reply with conservative token limits for low-RAM
-        reply = genai_client.transcribe_and_chat(cmd_file, system_instruction=system_instruction)
-        speak(engine, reply)
+
+        # First attempt to transcribe (local or provider) to detect commands like 'virtual mouse'
+        transcription = ""
+        try:
+            transcription = genai_client.transcribe_audio_local(cmd_file)
+        except Exception:
+            transcription = ""
+
+        # If user asked to open virtual mouse, launch it and return
+        if transcription and any(kw in transcription.lower() for kw in ["virtual mouse", "open virtual mouse", "mouse mode", "start virtual mouse"]):
+            # On Termux mobile, virtual mouse via webcam is often unsupported; warn user if so
+            if engine.config.is_termux:
+                speak(engine, "Virtual mouse requires a desktop environment with a webcam. This device may not support virtual mouse.")
+            else:
+                speak(engine, "Launching virtual mouse. Say 'exit' in the virtual mouse window or press q to quit.")
+                try:
+                    # Launch the bundled virtual mouse in a subprocess
+                    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "virtual_mouse", "main.py")])
+                except Exception as e:
+                    speak(engine, "Failed to launch virtual mouse: " + str(e))
+            clear_temp_file(cmd_file)
+            return
+
+        # Use wrapper to transcribe and reply with conservative token limits for low-RAM
+        reply = genai_client.transcribe_and_chat(cmd_file, system_instruction=system_instruction)
+        speak(engine, reply)
*** End Patch
