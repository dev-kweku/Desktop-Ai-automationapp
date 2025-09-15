import os
import json
from typing import Dict, Any
import logging

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
        self.logger = logging.getLogger(__name__)
        
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
            # Added folder_paths configuration
            "folder_paths": {
                "documents": "C:/Users/CALEB ASSAN/Documents",
                "downloads": "C:/Users/CALEB ASSAN/Downloads",
                "pictures": "C:/Users/CALEB ASSAN/Pictures",
                "music": "C:/Users/CALEB ASSAN/Music",
                "videos": "C:/Users/CALEB ASSAN/Videos",
                "desktop": "C:/Users/CALEB ASSAN/Desktop"
            },
            "email_address": "",
            "email_password": "",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "messaging_settings": {
                "whatsapp_wait_time": 15,
                "close_browser_after_send": True
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
                    # Merge with default config to ensure all keys exist
                    merged_config = {**self.default_config, **loaded_config}
                    
                    # Special handling for nested dictionaries
                    if "messaging_settings" in loaded_config:
                        merged_config["messaging_settings"] = {
                            **self.default_config["messaging_settings"],
                            **loaded_config["messaging_settings"]
                        }
                    
                    if "folder_paths" in loaded_config:
                        merged_config["folder_paths"] = {
                            **self.default_config["folder_paths"],
                            **loaded_config["folder_paths"]
                        }
                    
                    return merged_config
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
# # STANDLONE CONFIG  

# import os
# import json
# import sys
# import logging
# from typing import Dict, Any

# class Config:
#     def __init__(self):
#         # Determine if we're running as standalone executable
#         if getattr(sys, 'frozen', False):
#             # Running as compiled executable
#             self.base_path = os.path.dirname(sys.executable)
#             self.config_path = os.path.join(self.base_path, 'config.json')
#         else:
#             # Running as script
#             self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#             self.config_path = os.path.join(self.base_path, 'config.json')
        
#         # Set up logger
#         self.logger = logging.getLogger(__name__)
        
#         self.default_config = {
#             "model_name": "pattern_based",
#             "model_cache_dir": os.path.join(self.base_path, "assets", "models"),
#             "log_level": "INFO",
#             "log_file": os.path.join(self.base_path, "logs", "app.log"),
#             "allowed_directories": [
#                 os.path.expanduser("~/Documents"),
#                 os.path.expanduser("~/Downloads"),
#                 os.path.expanduser("~/Pictures"),
#                 os.path.expanduser("~/Music"),
#                 os.path.expanduser("~/Videos")
#             ],
#             "dangerous_commands": [
#                 "rm -rf",
#                 "format",
#                 "del /f /s /q",
#                 "shutdown",
#                 "restart"
#             ],
#             "application_paths": {
#                 "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
#                 "firefox": "C:/Program Files/Mozilla Firefox/firefox.exe",
#                 "notepad": "C:/Windows/System32/notepad.exe",
#                 "calculator": "calc.exe"
#             },
#             "email_address": "",
#             "email_password": "",
#             "smtp_server": "smtp.gmail.com",
#             "smtp_port": 587,
#             "messaging_settings": {
#                 "whatsapp_wait_time": 15,
#                 "close_browser_after_send": True
#             },
#             "twilio_account_sid": "",
#             "twilio_auth_token": "",
#             "twilio_phone_number": ""
#         }
#         self.config = self.load_config()
    
#     def load_config(self) -> Dict[str, Any]:
#         """Load configuration from file or use defaults"""
#         # Create necessary directories
#         self._create_necessary_directories()
        
#         if os.path.exists(self.config_path):
#             try:
#                 with open(self.config_path, 'r', encoding='utf-8') as f:
#                     loaded_config = json.load(f)
#                     # Merge with defaults, giving priority to loaded config
#                     merged_config = {**self.default_config, **loaded_config}
#                     self.logger.info(f"Configuration loaded from {self.config_path}")
#                     return merged_config
#             except json.JSONDecodeError as e:
#                 self.logger.error(f"Invalid JSON in config file: {str(e)}")
#                 return self.default_config
#             except Exception as e:
#                 self.logger.error(f"Error loading config: {str(e)}")
#                 return self.default_config
#         else:
#             # Create default config file if it doesn't exist
#             self.logger.info("Config file not found, creating default configuration")
#             self.save_config(self.default_config)
#             return self.default_config
    
#     def _create_necessary_directories(self):
#         """Create necessary directories for the application"""
#         directories = [
#             os.path.dirname(self.config_path),
#             os.path.join(self.base_path, "assets", "models"),
#             os.path.join(self.base_path, "logs"),
#             os.path.join(self.base_path, "screenshots")
#         ]
        
#         for directory in directories:
#             try:
#                 os.makedirs(directory, exist_ok=True)
#             except Exception as e:
#                 self.logger.error(f"Failed to create directory {directory}: {str(e)}")
    
#     def get(self, key: str, default: Any = None) -> Any:
#         """Get config value by key"""
#         return self.config.get(key, default)
    
#     def get_path(self, key: str, default: Any = None) -> Any:
#         """Get config value and ensure it's an absolute path"""
#         value = self.get(key, default)
#         if value and isinstance(value, str):
#             # If it's a relative path, make it absolute relative to base_path
#             if not os.path.isabs(value):
#                 return os.path.join(self.base_path, value)
#         return value
    
#     def save_config(self, new_config: Dict[str, Any]):
#         """Save updated configuration"""
#         try:
#             # Merge new config with existing
#             self.config = {**self.config, **new_config}
            
#             # Ensure directory exists
#             os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
#             # Save to file
#             with open(self.config_path, 'w', encoding='utf-8') as f:
#                 json.dump(self.config, f, indent=4, ensure_ascii=False)
            
#             self.logger.info(f"Configuration saved to {self.config_path}")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to save config: {str(e)}")
#             return False
    
#     def update_setting(self, key: str, value: Any):
#         """Update a single setting and save immediately"""
#         update = {key: value}
#         return self.save_config(update)
    
#     def get_email_config(self) -> Dict[str, str]:
#         """Get email configuration as a dictionary"""
#         return {
#             'email': self.get('email_address', ''),
#             'password': self.get('email_password', ''),
#             'smtp_server': self.get('smtp_server', 'smtp.gmail.com'),
#             'smtp_port': self.get('smtp_port', 587)
#         }
    
#     def get_twilio_config(self) -> Dict[str, str]:
#         """Get Twilio configuration as a dictionary"""
#         return {
#             'account_sid': self.get('twilio_account_sid', ''),
#             'auth_token': self.get('twilio_auth_token', ''),
#             'phone_number': self.get('twilio_phone_number', '')
#         }
    
#     def get_messaging_settings(self) -> Dict[str, Any]:
#         """Get messaging settings"""
#         return self.get('messaging_settings', {})
    
#     def is_email_configured(self) -> bool:
#         """Check if email is properly configured"""
#         email_config = self.get_email_config()
#         return bool(email_config['email'] and email_config['password'])
    
#     def is_twilio_configured(self) -> bool:
#         """Check if Twilio is properly configured"""
#         twilio_config = self.get_twilio_config()
#         return bool(twilio_config['account_sid'] and twilio_config['auth_token'] and twilio_config['phone_number'])

# # Utility function to get config instance
# def get_config() -> Config:
#     """Get a singleton configuration instance"""
#     if not hasattr(get_config, 'instance'):
#         get_config.instance = Config()
#     return get_config.instance