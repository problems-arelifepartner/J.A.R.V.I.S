# J.A.R.V.I.S
Personal assistant 
 
# Fork the tool befor using it and give the https://www.aistudio.google.com API in the api_key.txt file located inside the J.A.R.V.I.S/jarvis-terminal
```
pkg update && pkg upgrade -y
pkg install git python -y
git clone https://github.com/problems-arelifepartner/J.A.R.V.I.S.git
```
<p>
<img src= "https://github.com/problems-arelifepartner/J.A.R.V.I.S/blob/443d1475d644763b4631dfe32478eb5dea76a2f9/1000216972.png"/>
</p>

```
cd J.A.R.V.I.S
termux-setup-storage
cp 1000216972.png /sdcard/Download/
```
```
chmod 777 jarvis-terminal
cd jarvis-terminal
python setup.py
python jarvis.py
```
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



