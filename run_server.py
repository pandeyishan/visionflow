#!/usr/bin/env python3
"""VisionFlow Complete Setup and Server Launcher"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def install_dependencies():
    """Install required packages."""
    print("\n[*] Checking dependencies...")
    
    packages = {
        'flask': 'Flask',
        'flask_cors': 'flask-cors',
        'cv2': 'opencv-python',
        'numpy': 'numpy'
    }
    
    missing = []
    for pkg, pip_name in packages.items():
        try:
            __import__(pkg)
            print(f"  ✓ {pip_name}")
        except ImportError:
            print(f"  ✗ {pip_name} (missing)")
            missing.append(pip_name)
    
    if missing:
        print(f"\n[*] Installing missing packages: {', '.join(missing)}")
        for pkg in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])
        print("  ✓ All packages installed")
    
    return True

def start_server():
    """Start the VisionFlow server."""
    print("\n" + "="*70)
    print(" "*20 + "VISIONFLOW WEB SERVER")
    print("="*70)
    print("\n[*] Starting server...")
    
    # Change to DSL directory
    dsl_dir = Path(__file__).parent
    os.chdir(dsl_dir)
    
    # Start Flask server
    print("[✓] Server starting on http://localhost:5000\n")
    
    print("["*35 + "="*35 + "]")
    print("\n  Web UI:     http://localhost:5000")
    print("  Browser:    Opening automatically...\n")
    print("["*35 + "="*35 + "]\n")
    
    # Open browser after a short delay
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
    except:
        print("  [INFO] Please open http://localhost:5000 in your browser\n")
    
    # Import and run Flask
    from server import app
    
    print("[*] VisionFlow server is running!")
    print("[*] Press Ctrl+C to stop\n")
    
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n\n[*] Server stopped")

if __name__ == '__main__':
    try:
        install_dependencies()
        start_server()
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        sys.exit(1)
