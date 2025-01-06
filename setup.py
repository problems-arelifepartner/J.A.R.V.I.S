from cx_Freeze import setup, Executable

setup(
    name="JarvisAI",
    version="1.0",
    description="Jarvis AI Assistant",
    options={
        "build_exe": {
            "packages": ["tkinter", "pyttsx3", "speech_recognition", "openai"],
            "include_files": ["jarvis_interface.png"],  # Add any required files
        }
    },
    executables=[Executable("jarvis_ai_assistant.py", base="Win32GUI")],
)
