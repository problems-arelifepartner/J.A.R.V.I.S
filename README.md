# J.A.R.V.I.S
Personal assistant 


<p>
<img src= "https://github.com/problems-arelifepartner/J.A.R.V.I.S/blob/443d1475d644763b4631dfe32478eb5dea76a2f9/1000216972.png"/>
</p> 


<img src= "https://github.com/problems-arelifepartner/J.A.R.V.I.S/blob/b28cfc0065b64813658084d4510dff742f6c3429/IamIronMan.gif"/>



# J.A.R.V.I.S. (Just A Rather Very Intelligent System)

An immersive, voice-to-voice terminal assistant designed specifically to run inside the **Termux** environment on Android [1]. Utilizing Google's high-reasoning **Gemini 3.5 Pro** engine via the Google AI Studio free developer tier, J.A.R.V.I.S. is configured to operate entirely through voice-to-voice communication, integrating advanced emotional modeling, adaptive speech styling, and strict Android permission validation.

---

## Key Features

- **Strict Voice-to-Voice Loop:** Operating under a native Push-to-Talk format. There are no manual text inputs or visual text outputs of conversational replies; communication is fully vocal.
- **Contextual Emotional Processing:** Programmed to analyze vocal tone, urgency, and phrasing—adapting from logical reassurance (for stress) to witty dry humor (for normal operations) without breaking persona.
- **Hardware & Permission Gatekeeper:** Runs automated sweeps during startup to verify and request Storage, Microphone, and Android Text-to-Speech (TTS) integration [1], shutting down safely if permissions are missing.
- **Gemini 3.5 Pro Integration:** Leverages advanced free-tier reasoning models to handle complex analytical queries directly through Android's command line.

---

## System Requirements & Prerequisites

To execute this program, your Android device must have the following system integrations configured:

1. **Termux App:** Download and install Termux (it is recommended to use the latest builds from [F-Droid](https://f-droid.org/en/packages/com.termux/)).
2. **Termux:API Android App:** Install the companion **Termux:API** application from [F-Droid](https://f-droid.org/en/packages/com.termux.api/) to allow terminal scripts to access your phone's microphone, storage, and speech synthesis engines.
3. **Android System Permissions:** Open your Android device settings, go to **Apps -> Termux:API -> Permissions**, and ensure **Microphone** and **Storage** access are granted.

---

## Installation & Setup Guide

Execute the following commands sequence in your Termux terminal to set up the environment:

### Step 1: Update System Packages & Install Dependencies
Ensure your package lists are up to date and install the Git, Python, and Termux-API platform tools [1]:
```bash
pkg update && pkg upgrade -y
pkg install git python termux-api -y

git clone https://github.com/problems-arelifepartner/J.A.R.V.I.S.git
cd J.A.R.V.I.S

python setup.py

echo "YOUR_GEMINI_API_KEY_HERE" > api_key.txt

python jarvis.py

Voice Operation Sequence:
Upon starting, J.A.R.V.I.S. will perform system sweeps. If all permissions are approved, he will announce: "Uplink established, sir. Mainframe is in standby. Speak the activation phrase when ready."
Standby Mode: J.A.R.V.I.S. enters a passive, low-power listening cycle. The screen will read: [ STANDBY ] Monitoring environmental acoustic data....
Activation: Speak any of the trigger phrases clearly (e.g., "Hey Jarvis" or "Assemble").
Once triggered, the terminal shifts status to [✓] Trigger Word Detected. and J.A.R.V.I.S. will speak: "Always, sir. What is your directive?"
Command Delivery: The console displays >>> [ ACTIVE LISTENING ] <<<. State your command or question naturally within the 5.5-second recording window.
Processing & Feedback: J.A.R.V.I.S. processes the command, vocalizes the solution through your speakers, and automatically resets back to Standby Mode.
To shut down the script safely at any time, press CTRL + C on your terminal.
Troubleshooting Permissions
If J.A.R.V.I.S. fails during initialization, check for the following:
Storage Permission Error:
Run termux-setup-storage manually in the terminal, accept the Android system prompt, and restart the script.
Microphone Access Blocked (0 Bytes):
Open Android Settings -> Apps -> Termux:API -> Permissions and toggle Microphone to Allow.
No Voice Output (Silence):
Check that Google Text-to-Speech (or your device's default speech engine) is enabled in Android's Language & Input -> Text-to-speech output settings.

Copyright, Licensing & Legal Disclaimers
Open Source License
This project is licensed under the terms of the MIT License. You are free to modify, distribute, and utilize the software for personal, non-commercial purposes, provided the original copyright notice and permission consent are retained.
Trademark Disclaimer
J.A.R.V.I.S., Tony Stark, Stark Industries, and Iron Man are registered trademarks of Marvel Characters, Inc. and The Walt Disney Company.
This project is an independent, non-profit, open-source educational demonstration and creative tribute. It is not affiliated with, endorsed by, or associated with Marvel, Disney, or any of their partner subsidiaries.
API Usage Terms
This application utilizes Google AI Studio API keys. Users are responsible for adhering to the Google APIs Terms of Service and managing their own secure key storage.



