import os
import subprocess

def list_files(directory="."):
    """Lists files and directories in the specified path."""
    try:
        path = os.path.abspath(directory)
        items = os.listdir(path)
        return {"status": "success", "directory": path, "contents": items}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_file_content(filepath):
    """Reads and returns the text content of a local file safely."""
    try:
        path = os.path.abspath(filepath)
        if not os.path.exists(path):
            return {"status": "error", "message": "File not found."}
        with open(path, 'r', errors='ignore') as f:
            content = f.read(1500) # Cap at 1500 chars to avoid overwhelming context window
        return {"status": "success", "filepath": path, "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_system_command(command):
    """Executes safe custom shell commands locally and captures stdout."""
    try:
        # Array of forbidden destructive root components
        forbidden = ["rm -rf /", "mkfs", "dd", "shutdown", "reboot"]
        if any(bad in command for bad in forbidden):
            return {"status": "rejected", "message": "Command blocked by security protocols."}
            
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return {
            "status": "success",
            "stdout": result.stdout[:1000],
            "stderr": result.stderr[:500]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Map tools for the LLM Model integration
JARVIS_TOOLS = [list_files, read_file_content, execute_system_command]
