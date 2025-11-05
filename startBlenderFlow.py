import webbrowser
import subprocess
import os
import time

def launch_workflow(apps, urls):
    print("Starting your daily workflow...")
    
    # 1. Launch websites first (they load in the background)
    print("Opening critical websites...")
    for url in urls:
        webbrowser.open_new_tab(url)
        time.sleep(0.5) # Small delay to ensure browser handles them

    # 2. Launch local applications
    print("Launching applications...")
    for app_path in apps:
        try:
            # Use os.startfile for Windows, or subprocess for cross-platform
            if os.name == 'nt': # Windows
                os.startfile(app_path)
            else: # macOS/Linux
                subprocess.Popen([app_path])
        except FileNotFoundError:
            print(f"ERROR: Application not found at {app_path}")

# --- Your Custom Setup ---
CRITICAL_URLS = [
    "https://mail.google.com",
    "https://www.udemy.com/course/blender-creating-the-dune-ornithopter-from-start-to-finish/learn/lecture/32987980#overview"
]

CRITICAL_APPS = [
    #r"C:\Program Files\Microsoft VS Code\Code.exe", # Windows path example
    r"Z:\Blender\blender.exe"
]

launch_workflow(CRITICAL_APPS, CRITICAL_URLS)
print("Setup complete! Time to work.")