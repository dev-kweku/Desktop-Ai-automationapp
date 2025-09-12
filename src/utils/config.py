import os
import json
from typing import Dict, Any

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
        self.default_config = {
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
                "close_browser_after_send": True  # Changed from true to True
            },
            "twilio_account_sid": "",
            "twilio_auth_token": "",
            "twilio_phone_number": ""
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # JSON.load automatically converts true/false to True/False
                    return {**self.default_config, **loaded_config}
            except Exception as e:
                self.logger.error(f"Error loading config: {str(e)}")
                return self.default_config
        return self.default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by key"""
        return self.config.get(key, default)
    
    def save_config(self, new_config: Dict[str, Any]):
        """Save updated configuration"""
        self.config = {**self.config, **new_config}
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)