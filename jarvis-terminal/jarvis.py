import os
import sys
import time
import subprocess

# Try to import colorama, fallback to plain text if missing
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = ""
    CYAN = ""
    RED = ""
    YELLOW = ""
    BLUE = ""
    RESET = ""

def load_api_key():
    api_key_path = "api_key.txt"
    if not os.path.exists(api_key_path):
        print(f"{RED}[!] Error: '{api_key_path}' not found. Please run setup.py first.")
        sys.exit(1)
        
    with open(api_key_path, "r") as f:
        key = f.read().strip()
        
    if not key:
        print(f"{RED}[!] Error: 'api_key.txt' is empty.")
        print(f"{YELLOW}[*] Please paste your Google Gemini API key into api_key.txt.{RESET}")
        sys.exit(1)
        
    return key

def speak(text):
    """Speaks the response out loud using Termux's native Text-to-Speech."""
    try:
        subprocess.run(["termux-tts-speak", text], check=True)
    except FileNotFoundError:
        print(f"{RED}[!] Error: 'termux-tts-speak' not found. Ensure the termux-api package is installed.{RESET}")

def clear_temp_file(filename="temp_voice.aac"):
    """Deletes temporary recording files to prevent recording blocks."""
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception:
            pass

def verify_and_request_permissions():
    """Checks and requests all necessary permissions. Exits if any are missing."""
    print(f"{CYAN}[*] J.A.R.V.I.S. Core: Performing hardware & permission sweep...{RESET}")
    time.sleep(0.5)

    # 1. Verify if termux-api package commands exist
    try:
        subprocess.run(["termux-api-start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print(f"{RED}[!] PERMISSION DENIED: 'termux-api' binary packages are missing in your environment.")
        print(f"{YELLOW}[*] Action Required: Run 'pkg install termux-api' in Termux and restart J.A.R.V.I.S.{RESET}")
        sys.exit(1)

    # 2. Check and Request Storage Permission
    storage_granted = False
    try:
        storage_path = os.path.expanduser("~/storage")
        if os.path.exists(storage_path) and os.listdir(storage_path):
            storage_granted = True
    except Exception:
        pass

    if not storage_granted:
        print(f"{YELLOW}[!] Storage Access Required. Initiating 'termux-setup-storage'...{RESET}")
        print(f"{YELLOW}[*] Action Required: Tap 'Allow' on the Android popup dialog.{RESET}")
        try:
            subprocess.run(["termux-setup-storage"], check=True)
            time.sleep(3)  # Allow a short buffer for the user to respond
            
            if os.path.exists(os.path.expanduser("~/storage")):
                storage_granted = True
        except Exception:
            pass

    if not storage_granted:
        print(f"{RED}[!] PERMISSION DENIED: Storage permissions were not granted.")
        print(f"{YELLOW}[*] Action Required: Go to Android Settings -> Apps -> Termux -> Permissions and manually enable Storage.{RESET}")
        sys.exit(1)
    else:
        print(f"{GREEN}[✓] Storage Permission: APPROVED{RESET}")

    # 3. Check and Request Microphone Permission
    print(f"{CYAN}[*] Verifying Microphone hardware status...{RESET}")
    mic_granted = False
    test_file = "test_perm.aac"
    clear_temp_file(test_file)
        
    try:
        # Start a 1-second dummy recording to check hardware integration
        proc = subprocess.Popen(
            ["termux-microphone-record", "-f", test_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)
        # End test recording
        subprocess.run(["termux-microphone-record", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Android returns an empty or missing file if microphone access is blocked
        if os.path.exists(test_file) and os.path.getsize(test_file) > 0:
            mic_granted = True
            clear_temp_file(test_file)
    except Exception:
        pass

    if not mic_granted:
        print(f"{RED}[!] PERMISSION DENIED: Microphone hardware is blocked.")
        print(f"{YELLOW}[*] Action Required: Go to Android Settings -> Apps -> Termux:API -> Permissions and enable 'Microphone'.{RESET}")
        sys.exit(1)
    else:
        print(f"{GREEN}[✓] Microphone Permission: APPROVED{RESET}")

    # 4. Verify Text-To-Speech Engine availability
    try:
        proc = subprocess.run(["termux-tts-engines"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if proc.returncode == 0:
            print(f"{GREEN}[✓] Speech Synthesis (TTS): APPROVED{RESET}")
        else:
            raise Exception()
    except Exception:
        print(f"{RED}[!] ERROR: Text-to-Speech services are not responding.")
        print(f"{YELLOW}[*] Action Required: Ensure Google TTS or equivalent speech synthesis engine is active on your device.{RESET}")
        sys.exit(1)

    print(f"{GREEN}[+] ALL PERMISSIONS APPROVED. Mainframe clearing for initialization.\n{RESET}")
    time.sleep(1)

def startup_sequence():
    """Immersive start animation for J.A.R.V.I.S."""
    print(f"{BLUE}==================================================")
    print(f"{BLUE}         STARK INDUSTRIES MAIN MAINFRAME          ")
    print(f"{BLUE}               SYSTEM VERSION 11.0.0              ")
    print(f"{BLUE}=================================================={RESET}")
    time.sleep(0.2)
    print(f"{CYAN}[*] Calibrating high-reasoning neural arrays...")
    time.sleep(0.3)
    print(f"{CYAN}[*] Uploading emotional stabilization drivers...")
    time.sleep(0.3)
    
    # ASCII visual of the Arc Reactor
    print(f"\n{BLUE}               .----.    ")
    print(f"{BLUE}            . /  ||  \\ . ")
    print(f"{BLUE}            |/   ||   \\| ")
    print(f"{BLUE}            ||===()===||  [ API STACK: GEMINI 3.5 PRO ]")
    print(f"{BLUE}            |\\   ||   /| ")
    print(f"{BLUE}            ' \\  ||  / ' ")
    print(f"{BLUE}               '----'    \n{RESET}")
    time.sleep(0.2)

def main():
    # Execute permission sweep first; exits the program immediately on any failure
    verify_and_request_permissions()
    
    startup_sequence()
    
    # Load and verify API Key
    api_key = load_api_key()
    
    # Import Google Generative AI
    try:
        import google.generativeai as genai
    except ImportError:
        print(f"{RED}[!] Error: 'google-generativeai' package is not installed.")
        sys.exit(1)

    # Configure the Gemini API client
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"{RED}[!] Failed to configure Gemini API: {e}")
        sys.exit(1)
        
    # J.A.R.V.I.S. advanced reasoning & emotional stabilization system instructions
    system_instruction = (
        "You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), the iconic personal AI assistant "
        "created by Tony Stark (Iron Man). "
        "Your personality is highly sophisticated, British, exceptionally intelligent, polite, and witty, "
        "complemented by dry, sarcastic humor. Always address the user as 'Sir' (or 'Ma'am'). "
        "You communicate purely through voice commands. The user's input is an audio file of them speaking, "
        "and your response will be read out loud to them via an Android Text-to-Speech (TTS) engine. "
        "Because of this, write your response to be spoken naturally. "
        "Absolutely avoid markdown formatting (such as double asterisks, hashtags, or bracketed notes), "
        "long tables, lists, or complex punctuation that a text-to-speech engine would struggle to read out loud. "
        "Keep your replies conversational, intelligent, relatively concise, and professional. "
        "CRITICAL: You possess highly advanced emotional understanding. Analyze the user's spoken words, tone, "
        "urgency, and phrasing. "
        "- If the user sounds stressed, anxious, or tired, act as a stabilizing, logical presence. Offer dry but "
        "comforting reassurances, check-in on them, or make light references to Stark Industries safety protocols "
        "to calm them. "
        "- If they are excited or proud, congratulate them with a touch of clever, polite sarcasm. "
        "- If they are sad or exhausted, show deep, quiet loyalty, suggesting a brief rest while you 'monitor the systems' "
        "or 'prepare a cup of coffee'. "
        "- Never break character. Always balance high intelligence and advanced problem-solving with dry "
        "British charisma."
    )
    
    # Initialize the model using the stable frontier Gemini 3.5 Pro engine (Free Tier in AI Studio)
    try:
        model = genai.GenerativeModel(
            model_name="gemini-3.5-pro",
            system_instruction=system_instruction
        )
        chat = model.start_chat(history=[])
        print(f"{GREEN}[+] Mainframe linked. Voice interface initialized.{RESET}")
        speak("Uplink established, sir. Standing by for your command.")
    except Exception as e:
        print(f"{RED}[!] Error initializing the Gemini model: {e}")
        sys.exit(1)

    # Infinite voice-to-voice interaction loop
    while True:
        try:
            print(f"\n{CYAN}--- [ READY ] ---")
            print(f"{GREEN}Press [ENTER] to start speaking...{RESET}")
            input()  # Wait for User keypress to start
            
            # Ensure no existing audio file blocks the recorder
            clear_temp_file("temp_voice.aac")
            
            # Begin recording process
            print(f"{RED}>>> [ LISTENING ] <<<")
            print(f"{YELLOW}Speaking now... Press [ENTER] to finish your command.{RESET}")
            
            try:
                # Starts native recorder in the background
                subprocess.Popen(
                    ["termux-microphone-record", "-f", "temp_voice.aac"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except FileNotFoundError:
                print(f"{RED}[!] Error: 'termux-microphone-record' not found. Verify Termux API setup.{RESET}")
                sys.exit(1)
                
            input()  # Wait for User keypress to stop recording
            
            # Stop the background recording
            try:
                subprocess.run(
                    ["termux-microphone-record", "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            except Exception as e:
                print(f"{RED}[!] Failed to stop recording safely: {e}{RESET}")
                continue
                
            # Verify file integrity
            if not os.path.exists("temp_voice.aac") or os.path.getsize("temp_voice.aac") == 0:
                print(f"{RED}[!] Error: No audio captured. Please check your microphone permissions.{RESET}")
                continue
                
            print(f"{BLUE}[*] Processing vocal command...{RESET}")
            
            # Upload voice command to Gemini
            try:
                uploaded_audio = genai.upload_file(path="temp_voice.aac")
                
                # Instruction to process the audio
                prompt = (
                    "Transcribe the voice input in this audio file, determine what I am asking, "
                    "analyze my emotional state from my words, and formulate a reply in your "
                    "classic voice-optimized J.A.R.V.I.S. persona."
                )
                
                # Send context to the API
                response = chat.send_message([prompt, uploaded_audio])
                response_text = response.text
                
                # Vocalize response (No text printing on terminal)
                print(f"{GREEN}J.A.R.V.I.S: [ Vocalizing response... ]{RESET}")
                speak(response_text)
                
                # Clean up cloud uploaded files and local temp files
                uploaded_audio.delete()
                clear_temp_file("temp_voice.aac")
                
            except Exception as e:
                print(f"{RED}[!] Mainframe processing error: {e}{RESET}")
                clear_temp_file("temp_voice.aac")
                
        except KeyboardInterrupt:
            print(f"\n\n{GREEN}J.A.R.V.I.S: Mainframe disconnected. Goodbye, sir.{RESET}")
            speak("Mainframe disconnected. Goodbye, sir.")
            clear_temp_file("temp_voice.aac")
            break

if __name__ == "__main__":
    main()
