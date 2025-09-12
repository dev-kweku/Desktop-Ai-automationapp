import os
import shutil
import PyInstaller.__main__
import sys

def build_application():
    print("Building Desktop AI Assistant...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Create necessary directories
    os.makedirs('assets/icons', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Create a default config if it doesn't exist
    if not os.path.exists('src/utils/config.json'):
        default_config = {
            "model_name": "pattern_based",
            "model_cache_dir": "./assets/models",
            "log_level": "INFO",
            "log_file": "./logs/app.log",
            "allowed_directories": [
                "~/Documents",
                "~/Downloads",
                "~/Pictures",
                "~/Music",
                "~/Videos"
            ],
            "dangerous_commands": [
                "rm -rf",
                "format",
                "del /f /s /q",
                "shutdown",
                "restart"
            ],
            "application_paths": {
                "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "firefox": "C:/Program Files/Mozilla Firefox/firefox.exe",
                "notepad": "C:/Windows/System32/notepad.exe",
                "calculator": "calc.exe"
            },
            "email_address": "",
            "email_password": "",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "messaging_settings": {
                "whatsapp_wait_time": 15,
                "close_browser_after_send": True
            }
        }
        import json
        with open('src/utils/config.json', 'w') as f:
            json.dump(default_config, f, indent=4)
    
    # Build using PyInstaller
    PyInstaller.__main__.run([
        'build.spec',
        '--clean',
        '--noconfirm'
    ])
    
    print("Build completed! Executable is in the 'dist' folder.")

if __name__ == "__main__":
    build_application()