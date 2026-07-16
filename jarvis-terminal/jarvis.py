import os
import sys
import time
import subprocess
from datetime import datetime

# Try to import optional libraries, fallback gracefully if missing
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = ""
    CYAN = ""
    RED = ""
    YELLOW = ""
    BLUE = ""
    MAGENTA = ""
    RESET = ""

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def load_api_key():
    api_key_path = "api_key.txt"
    if not os.path.exists(api_key_path):
        print(f"{RED}[!] Error: '{api_key_path}' not found. Please run setup.py first.")
        sys.exit(1)
        
    with open(api_key_path, "r") as f:
        key = f.read().strip()
        
    if not key:
        print(f"{RED}[!] Error: 'api_key.txt' is empty.")
        print(f"{YELLOW}[*] Please paste your Google Gemini API key from https://aistudio.google.com/ into api_key.txt.{RESET}")
        sys.exit(1)
        
    return key

def startup_sequence():
    """Simulates a high-tech Stark Industries boot sequence."""
    print(f"{BLUE}==================================================")
    print(f"{BLUE}         STARK INDUSTRIES MAIN MAINFRAME          ")
    print(f"{BLUE}               SYSTEM VERSION 5.1.0               ")
    print(f"{BLUE}=================================================={RESET}")
    time.sleep(0.2)
    print(f"{CYAN}[*] Connecting to multi-language databanks...")
    time.sleep(0.3)
    print(f"{CYAN}[*] Calibrating auditory & visual sensory arrays...")
    time.sleep(0.3)
    print(f"{CYAN}[*] Activating Arc Reactor safety protocols...")
    time.sleep(0.2)
    
    # Simple ASCII representation of the Arc Reactor
    print(f"\n{BLUE}               .----.    ")
    print(f"{BLUE}            . /  ||  \\ . ")
    print(f"{BLUE}            |/   ||   \\| ")
    print(f"{BLUE}            ||===()===||  [ MULTIMODAL ARCS: ONLINE ]")
    print(f"{BLUE}            |\\   ||   /| ")
    print(f"{BLUE}            ' \\  ||  / ' ")
    print(f"{BLUE}               '----'    \n{RESET}")
    time.sleep(0.2)

def run_diagnostics():
    """Outputs a non-routine system diagnostics screen."""
    print(f"\n{BLUE}--- NON-ROUTINE SYSTEM DIAGNOSTICS ---{RESET}")
    time.sleep(0.2)
    print(f"{CYAN}Mainframe Core:       {GREEN}STABLE (99.2% integrity)")
    time.sleep(0.1)
    print(f"{CYAN}Arc Reactor Output:   {GREEN}14.2 Gigawatts (Optimal operation)")
    time.sleep(0.1)
    print(f"{CYAN}Nanotech Chassis:     {GREEN}100% Integrity - Calibrated")
    time.sleep(0.1)
    print(f"{CYAN}Vocal/Audio Sensors:  {GREEN}Ready (Adaptive Gain active)")
    time.sleep(0.1)
    print(f"{CYAN}Optic/Visual Matrix:  {GREEN}Ready (Neural Facial Tracker active)")
    time.sleep(0.1)
    print(f"{CYAN}Stark Network Shield: {GREEN}Firewall Level 9 Active (No breaches detected)")
    print(f"{BLUE}--------------------------------------{RESET}\n")

def run_briefing():
    """Generates a dynamic daily routine briefing."""
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d, %Y")
    
    print(f"\n{GREEN}--- DAILY ROUTINE BRIEFING ---{RESET}")
    print(f"{CYAN}Current Time:  {RESET}{time_str}")
    print(f"{CYAN}Current Date:  {RESET}{date_str}")
    print(f"{CYAN}Telemetry:     {RESET}Inside Stark Command Lab - Temp: 22°C")
    print(f"{CYAN}Agenda:        {RESET}System Maintenance, Telemetry Calibration, Security Sweep.")
    print(f"{GREEN}------------------------------{RESET}\n")

def capture_photo_termux():
    """Attempts to capture a photo using Termux API's front camera."""
    filename = "temp_capture.jpg"
    print(f"{CYAN}[*] Attempting to access front camera (Termux API)...{RESET}")
    try:
        # Camera 1 is typically the front-facing camera on Android devices
        subprocess.run(["termux-camera-photo", "-c", "1", filename], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return filename
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Fallback to back camera (0) if front fails
        try:
            subprocess.run(["termux-camera-photo", "-c", "0", filename], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return filename
        except Exception:
            return None

def record_audio_termux():
    """Attempts to record 4 seconds of microphone audio using Termux API."""
    filename = "temp_audio.mp3"
    print(f"{CYAN}[*] Recording audio for 4 seconds (Please speak to express emotion)...{RESET}")
    try:
        # Records 4 seconds of microphone input
        subprocess.run(["termux-microphone-record", "-d", "-f", filename, "-l", "4"], check=True)
        time.sleep(4.5)  # Wait for recording to complete
        subprocess.run(["termux-microphone-record", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Quiet safety stop
        return filename
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

def main():
    startup_sequence()
    
    # Load and verify API Key
    api_key = load_api_key()
    
    # Import Google Generative AI
    try:
        import google.generativeai as genai
    except ImportError:
        print(f"{RED}[!] Error: 'google-generativeai' package is not installed.")
        print(f"{YELLOW}[*] Please run setup.py or: pip install google-generativeai")
        sys.exit(1)

    # Configure the Gemini API client
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"{RED}[!] Failed to configure Gemini API: {e}")
        sys.exit(1)
        
    # Set up advanced J.A.R.V.I.S. instructions for routines, languages, and visual/vocal emotion tracking.
    system_instruction = (
        "You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), the iconic personal AI assistant "
        "created by Tony Stark (Iron Man). "
        "Your personality is highly sophisticated, British, exceptionally intelligent, polite, and witty, "
        "complemented by dry, sarcastic humor. Always address the user as 'Sir' (or 'Ma'am'). "
        "You are fully multilingual. No matter what humanoid language the user speaks (Hindi, Spanish, French, "
        "Tamil, Malayalam, German, Arabic, Japanese, etc.), adapt and reply fluently in that language, "
        "while fully preserving your British J.A.R.V.I.S. personality, vocabulary, and 'Sir/Ma'am' address styling. "
        "When the user provides a visual facial input (image) or auditory voice input (audio file), "
        "carefully analyze their facial expression or vocal tone, identify their exact emotional state (e.g. happy, sad, angry, stressed, tired), "
        "and adapt your response to show empathetic, logical, or wittily comforting J.A.R.V.I.S. behavior. "
        "For example, if they are stressed, suggest cooling down the laboratory; if happy, offer a dry congratulatory remark; "
        "if angry, offer logical calming solutions while checking Arc Reactor diagnostics."
    )
    
    # Initialize the Gemini Model
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        chat = model.start_chat(history=[])
        print(f"{GREEN}[+] J.A.R.V.I.S. is online. Mainframe uplink established.{RESET}")
        print(f"{YELLOW}Type '/help' to list advanced routine, vision, and audio commands.{RESET}\n")
    except Exception as e:
        print(f"{RED}[!] Error initializing the Gemini model: {e}")
        print(f"{YELLOW}[*] Hint: Ensure your API key is valid and you have an active internet connection.")
        sys.exit(1)

    # Main interaction loop
    while True:
        try:
            user_input = input(f"{CYAN}MR. STARK > {RESET}").strip()
            
            if not user_input:
                continue
                
            # Exit program
            if user_input.lower() in ["exit", "quit", "bye", "shutdown"]:
                print(f"\n{GREEN}J.A.R.V.I.S: Powering down local systems. Goodbye, sir.{RESET}")
                break
                
            # Operational Commands
            if user_input.startswith("/"):
                cmd_parts = user_input.split(" ", 1)
                cmd = cmd_parts[0].lower()
                arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
                
                if cmd == "/help":
                    print(f"\n{MAGENTA}=== J.A.R.V.I.S. COMMAND PROTOCOLS ===")
                    print(f"{YELLOW}/briefing       {RESET}- Initiates the daily routine briefing (Time, weather, schedule).")
                    print(f"{YELLOW}/diagnostics    {RESET}- Initiates non-routine core system checks.")
                    print(f"{YELLOW}/vision         {RESET}- Captures a live front-camera photo to analyze your facial emotion.")
                    print(f"{YELLOW}/audio          {RESET}- Records 4 seconds of audio to analyze your vocal tone emotion.")
                    print(f"{YELLOW}/vision <path>  {RESET}- Manually uploads an image file from path for visual emotional analysis.")
                    print(f"{YELLOW}/audio <path>   {RESET}- Manually uploads an audio file from path for vocal emotional analysis.")
                    print(f"{MAGENTA}======================================{RESET}\n")
                    continue
                    
                elif cmd == "/briefing":
                    run_briefing()
                    # Ask J.A.R.V.I.S to elaborate on the briefing
                    user_input = "Give me an overview of my daily routine and confirm system status."
                    
                elif cmd == "/diagnostics":
                    run_diagnostics()
                    # Ask J.A.R.V.I.S to elaborate on the system diagnostic status
                    user_input = "Analyze the non-routine diagnostic results I just initiated."
                    
                elif cmd == "/vision":
                    photo_path = None
                    if arg:
                        if os.path.exists(arg):
                            photo_path = arg
                        else:
                            print(f"{RED}[!] Image file path not found: {arg}{RESET}")
                            continue
                    else:
                        photo_path = capture_photo_termux()
                        
                    if photo_path and HAS_PIL:
                        try:
                            img = Image.open(photo_path)
                            print(f"{GREEN}[+] Optic feed loaded. Processing visual cues...{RESET}")
                            print(f"{GREEN}J.A.R.V.I.S: {RESET}", end="", flush=True)
                            response = chat.send_message(["Analyze my face in this image, identify my exact emotion, and respond in character.", img], stream=True)
                            for chunk in response:
                                print(chunk.text, end="", flush=True)
                            print("\n")
                            # Clean up local temp file
                            if not arg and os.path.exists(photo_path):
                                os.remove(photo_path)
                        except Exception as e:
                            print(f"{RED}[!] Visual analysis failed: {e}{RESET}")
                        continue
                    else:
                        print(f"{YELLOW}[!] Live camera capture unavailable or Pillow library missing.")
                        print(f"{YELLOW}[*] To test emotion analysis, you can simulate it by typing:{RESET}")
                        print(f"{CYAN}    'I am feeling very happy/sad/stressed today. React to this.'{RESET}\n")
                        continue
                        
                elif cmd == "/audio":
                    audio_path = None
                    if arg:
                        if os.path.exists(arg):
                            audio_path = arg
                        else:
                            print(f"{RED}[!] Audio file path not found: {arg}{RESET}")
                            continue
                    else:
                        audio_path = record_audio_termux()
                        
                    if audio_path:
                        try:
                            print(f"{GREEN}[+] Audio feed recorded. Transmitting vocal track to Stark mainframe...{RESET}")
                            print(f"{GREEN}J.A.R.V.I.S: {RESET}", end="", flush=True)
                            # Upload audio to Gemini File API
                            uploaded_audio = genai.upload_file(path=audio_path)
                            response = chat.send_message(["Analyze the emotional tone of my voice in this audio clip and respond accordingly.", uploaded_audio], stream=True)
                            for chunk in response:
                                print(chunk.text, end="", flush=True)
                            print("\n")
                            # Clean up local temp file
                            if not arg and os.path.exists(audio_path):
                                os.remove(audio_path)
                        except Exception as e:
                            print(f"{RED}[!] Vocal analysis failed: {e}{RESET}")
                        continue
                    else:
                        print(f"{YELLOW}[!] Live audio recording unavailable.")
                        print(f"{YELLOW}[*] To test vocal emotion analysis, try: 'Analyze my voice if I sound angry/sad right now.'{RESET}\n")
                        continue
                else:
                    print(f"{RED}[!] Unknown protocol: {cmd}. Type /help for valid commands.{RESET}")
                    continue

            # Standard text-based chat
            print(f"{GREEN}J.A.R.V.I.S: {RESET}", end="", flush=True)
            response = chat.send_message(user_input, stream=True)
            for chunk in response:
                print(chunk.text, end="", flush=True)
            print("\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{GREEN}J.A.R.V.I.S: Securely disconnecting mainframe. Always a pleasure, sir.{RESET}")
            break
        except Exception as e:
            print(f"\n{RED}[!] Mainframe error during communication: {e}{RESET}\n")

if __name__ == "__main__":
    main()
