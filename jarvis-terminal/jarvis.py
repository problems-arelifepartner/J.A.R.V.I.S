import os
import json
from google import genai
from google.genai import types
from config import Config
from audio_engine import AudioEngine
from tools import JARVIS_TOOLS

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
        self.client = genai.Client(api_key=self.config.api_key)
        self.chat_config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=JARVIS_TOOLS,
            temperature=0.7
        )
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=self.chat_config
        )

    def run(self):
        self.audio.speak("Systems initialized and online, sir. Standing by for your command.")

        while True:
            try:
                if self.audio.wait_for_wake_word("jarvis"):
                    self.audio.speak("Yes, sir?")
                    query = self.audio.listen()

                    if not query:
                        self.audio.speak("I didn't catch that, sir. Returning to standby.")
                        continue

                    if any(exit_phrase in query.lower() for exit_phrase in ["go to sleep", "shutdown", "exit"]):
                        self.audio.speak("Powering down systems. Goodbye, sir.")
                        break

                    print("[Processing Request...]")
                    response = self.chat.send_message(query)

                    if response.text:
                        self.audio.speak(response.text)

            except KeyboardInterrupt:
                self.audio.speak("Terminating program loops safely.")
                break
            except Exception as e:
                print(f"\n[Core Fault Handler] {e}")
                self.audio.speak("I encountered an internal processing variance. Resetting to standby.")

if __name__ == "__main__":
    jarvis = JarvisCore()
    jarvis.run()
