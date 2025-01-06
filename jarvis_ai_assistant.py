import tkinter as tk
from PIL import Image, ImageTk
import openai
import pyttsx3
import speech_recognition as sr
import os
import platform
from cx_Freeze import setup, Executable

# Set your OpenAI API key
openai.api_key = "your_openai_api_key_here"

# Function to use GPT for generating responses
def chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Function to convert text to speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "I didn't catch that."
        except sr.RequestError:
            return "Speech service error."

# Function to handle user input
def handle_command():
    command = listen()
    if command:
        response = chatgpt_response(command)
        speak(response)
        output_label.config(text=response)

# Check for admin/root privileges
def check_admin():
    if platform.system() == "Windows":
        if not os.geteuid() == 0:
            print("Please run the script as an administrator.")
            exit()
    elif os.geteuid() != 0:
        print("Please run the script as root.")
        exit()

# Create the GUI
def create_gui():
    root = tk.Tk()
    root.title("Jarvis AI Assistant")

    # Load and display the interface image
    try:
        img = Image.open("jarvis_interface.png")  # Replace with your saved image file
        img = img.resize((800, 600), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(root, image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.pack()
    except Exception as e:
        print(f"Error loading image: {e}")

    # Add a text area for output
    global output_label
    output_label = tk.Label(root, text="Hello, I am Jarvis. How can I assist you?", font=("Arial", 14), bg="black", fg="cyan", wraplength=700)
    output_label.pack(pady=20)

    # Add a button to listen for commands
    listen_button = tk.Button(root, text="Speak to Jarvis", command=handle_command, font=("Arial", 14), bg="blue", fg="white")
    listen_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    check_admin()  # Ensure the script is running with admin/root privileges
    create_gui()

# Setup script for converting the application to an executable
setup(
    name="JarvisAI",
    version="1.0",
    description="Jarvis AI Assistant",
    executables=[Executable("jarvis_ai_assistant.py", base=None)],
)


