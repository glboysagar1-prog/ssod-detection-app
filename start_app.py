#!/usr/bin/env python3

import subprocess
import sys
import os

def main():
    # Change to the project directory
    os.chdir("/Users/sagar/Desktop/ssod_detection_app")
    
    # Start the Streamlit app
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "app.py", 
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ]
    
    print("Starting SSOD Detection App...")
    print("Access the app at: http://localhost:8501")
    
    # Run the command
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        stdout, stderr = process.communicate()
        print("STDOUT:", stdout.decode())
        print("STDERR:", stderr.decode())
    except KeyboardInterrupt:
        process.terminate()
        print("App stopped.")

if __name__ == "__main__":
    main()