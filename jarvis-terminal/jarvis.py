import os
import json
import google.generativeai as genai
from config import Config
from audio_engine import AudioEngine
from tools import JARVIS_TOOLS, list_files, read_file_content, execute_system_command

# System guidelines handling persona and emotional response rules
SYSTEM_INSTRUCTION = """
You are J.A.R.V.I.S., an advanced AI assistant inspired by Iron Man. 
Your tone is sophisticated, brilliantly intelligent, crisp, and slightly witty with a British cadence.

Crucial Directives:
1. Emotion Monitoring: Closely analyze the emotional context, frustration, excitement, or urgency behind the user's spoken inputs. Adapt your responses to mirror or soothe their state dynamically.
2. Tool Execution: You have direct access to tools for checking files and running terminal commands. Use them whenever requested without explaining the tool choice. Keep descriptions of command outcomes concise.
3. Keep all vocal responses brief, structured, and clear. Avoid verbose blocks of text.
"""

class JarvisCore:
    def __init__(self):
        self.config = Config()
        self.audio = AudioEngine(self.config)
        
        # Configure Gemini Client
        genai.configure(api_key=self.config.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # Highly responsive for real-time voice latency
            system_instruction=SYSTEM_INSTRUCTION,
            tools=JARVIS_TOOLS
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def run(self):
        self.audio.speak("Systems initialized and online, sir. How may I assist you today?")
        
        while True:
            try:
                query = self.audio.listen()
                
                if not query:
                    continue
                
                # Check for explicit shutdown phrase
                if any(exit_phrase in query.lower() for exit_phrase in ["go to sleep", "shutdown jarvis", "exit"]):
                    self.audio.speak("Powering down systems. Goodbye, sir.")
                    break
                
                # Process thought through Gemini with automatic tool orchestration
                response = self.chat.send_message(query)
                
                if response.text:
                    self.audio.speak(response.text)
                    
            except KeyboardInterrupt:
                self.audio.speak("Terminating program loops safely.")
                break
            except Exception as e:
                print(f"\n[Core Fault Handler] {e}")
                self.audio.speak("I encountered an internal processing variance, sir. Retrying loop.")

if __name__ == "__main__":
    jarvis = JarvisCore()
    jarvis.run()
