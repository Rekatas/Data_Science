import subprocess
import sys
import os
from pathlib import Path

app = Path(__file__).resolve().parent / "Visualizations" / "App.py"

# Windows
if sys.platform == "win32":
    subprocess.Popen(
        f'start cmd /k "streamlit run {app}"',
        shell=True
    )
# macOS
elif sys.platform == "darwin":
    script = f'tell application "Terminal" to do script "streamlit run {app}"'
    subprocess.Popen(["osascript", "-e", script])
# Linux
else:
    subprocess.Popen(
        ["x-terminal-emulator", "-e", f"streamlit run {app}"]
    )
