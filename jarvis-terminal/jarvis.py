import os
import sys

# Try to import colorama for terminal styling; fallback to plain text if unavailable
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = ""
    CYAN = ""
    RED = ""
    YELLOW = ""
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
        print(f"{YELLOW}[*] Please paste your Google Gemini API key from https://aistudio.google.com/ into api_key.txt.{RESET}")
        sys.exit(1)
        
    return key

def main():
    print(f"{CYAN}=============================================")
    print(f"{CYAN}             J.A.R.V.I.S. TERMINAL            ")
    print(f"{CYAN}============================================={RESET}")
    
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
        
    # Set up J.A.R.V.I.S persona and system environment instructions
    system_instruction = (
        "You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), a highly intelligent, "
        "helpful, polite, and technically proficient terminal assistant. Speak concisely, "
        "professionally, and address the user respectfully. "
        "You are running within a Termux/Android command-line environment."
    )
    
    # Initialize the modern, fast Gemini model
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        chat = model.start_chat(history=[])
        print(f"{GREEN}[+] J.A.R.V.I.S. is online and ready.{RESET}")
        print(f"{YELLOW}Type 'exit', 'quit', or 'bye' to shut down.{RESET}\n")
    except Exception as e:
        print(f"{RED}[!] Error initializing the Gemini model: {e}")
        print(f"{YELLOW}[*] Hint: Ensure your API key is valid and you have an active internet connection.")
        sys.exit(1)

    # Main interaction loop
    while True:
        try:
            user_input = input(f"{CYAN}User > {RESET}").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"\n{GREEN}[+] J.A.R.V.I.S: Goodbye, sir.{RESET}")
                break
                
            print(f"{GREEN}J.A.R.V.I.S: {RESET}", end="", flush=True)
            
            # Send context to the model and stream the reply
            response = chat.send_message(user_input, stream=True)
            for chunk in response:
                print(chunk.text, end="", flush=True)
            print("\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{GREEN}[+] J.A.R.V.I.S: System shutting down safely. Goodbye, sir.{RESET}")
            break
        except Exception as e:
            print(f"\n{RED}[!] An error occurred during communication: {e}{RESET}\n")

if __name__ == "__main__":
    main()
