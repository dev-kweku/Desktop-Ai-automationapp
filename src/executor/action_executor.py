import os
import subprocess
import logging
import pyautogui
import psutil
from typing import Dict, Any
from src.utils.security import SecurityManager
from src.utils.config import Config
from src.integrations.messaging import MessagingIntegration
from src.integrations.web_control import WebController
from src.integrations.phone_control import PhoneIntegration

class ActionExecutor:
    def __init__(self, config: Config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.security = SecurityManager(config)
        self.messaging = MessagingIntegration()
        self.web_controller = WebController()
        self.phone_integration = PhoneIntegration()
    
    def execute(self, intent_data: Dict[str, Any]) -> str:
        """Execute action based on parsed intent"""
        intent = intent_data.get("intent", "unknown")
        params = intent_data.get("parameters", {})
        
        self.logger.info(f"Executing intent: {intent} with params: {params}")
        
        try:
            if intent == "open_application":
                return self.open_application(params)
            elif intent == "open_folder":
                return self.open_folder(params)
            elif intent == "create_file":
                return self.create_file(params)
            elif intent == "create_folder":
                return self.create_folder(params)
            elif intent == "delete_file":
                return self.delete_file(params)
            elif intent == "delete_folder":
                return self.delete_folder(params)
            elif intent == "rename_file":
                return self.rename_file(params)
            elif intent == "rename_folder":
                return self.rename_folder(params)
            elif intent == "take_screenshot":
                return self.take_screenshot(params)
            elif intent == "open_browser":
                return self.open_browser(params)
            elif intent == "search_web":
                return self.search_web(params)
                elif intent == "send_whatsapp":
                return self.send_whatsapp(params)
            elif intent == "send_email":
                return self.send_email(params)
            elif intent == "make_call":
                return self.make_call(params)
            else:
                return "Sorry, I didn't understand that command."
                
        except Exception as e:
            self.logger.error(f"Error executing action: {str(e)}")
            return f"Error: {str(e)}"
    
    def open_application(self, params: Dict[str, Any]) -> str:
        app_name = params.get("application", "")
        app_paths = self.config.get("application_paths", {})
        
        if app_name in app_paths:
            try:
                subprocess.Popen(app_paths[app_name])
                return f"Opened {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {str(e)}"
        else:
            return f"Application '{app_name}' not configured"
    
    def open_folder(self, params: Dict[str, Any]) -> str:
        folder_name = params.get("folder", "")
        folder_map = {
            "documents": os.path.expanduser("~/Documents"),
            "downloads": os.path.expanduser("~/Downloads"),
            "pictures": os.path.expanduser("~/Pictures"),
            "music": os.path.expanduser("~/Music"),
            "videos": os.path.expanduser("~/Videos"),
            "desktop": os.path.expanduser("~/Desktop")
        }
        
        if folder_name in folder_map:
            folder_path = folder_map[folder_name]
            if os.path.exists(folder_path):
                os.startfile(folder_path)
                return f"Opened {folder_name} folder"
            else:
                return f"{folder_name} folder doesn't exist"
        else:
            return "Specified folder not supported"
    
    def create_file(self, params: Dict[str, Any]) -> str:
        filename = params.get("filename", "new_file.txt")
        documents_path = os.path.expanduser("~/Documents")
        file_path = os.path.join(documents_path, filename)
        
        if not self.security.is_safe_path(file_path):
            return "Cannot create file in this location for security reasons"
        
        try:
            with open(file_path, 'w') as f:
                f.write("")
            return f"Created file: {filename}"
        except Exception as e:
            return f"Failed to create file: {str(e)}"
    
    def create_folder(self, params: Dict[str, Any]) -> str:
        folder_name = params.get("folder", "New Folder")
        documents_path = os.path.expanduser("~/Documents")
        folder_path = os.path.join(documents_path, folder_name)
        
        if not self.security.is_safe_path(folder_path):
            return "Cannot create folder in this location for security reasons"
        
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"Created folder: {folder_name}"
        except Exception as e:
            return f"Failed to create folder: {str(e)}"
    
    def delete_file(self, params: Dict[str, Any]) -> str:
        filename = params.get("filename", "")
        if not filename:
            return "No filename specified"
        
        documents_path = os.path.expanduser("~/Documents")
        file_path = os.path.join(documents_path, filename)
        
        if not self.security.is_safe_path(file_path):
            return "Cannot delete file from this location for security reasons"
        
        if not os.path.exists(file_path):
            return f"File {filename} doesn't exist"
        
        try:
            os.remove(file_path)
            return f"Deleted file: {filename}"
        except Exception as e:
            return f"Failed to delete file: {str(e)}"

    def send_whatsapp(self, params: Dict[str, Any]) -> str:
        phone = params.get("phone", "")
        message = params.get("message", "Hello from AI Assistant")
        
        if not phone:
            return "Please specify a phone number to send WhatsApp message to."
        
        return self.messaging.send_whatsapp_message(phone, message)
    
    def send_email(self, params: Dict[str, Any]) -> str:
        recipient = params.get("email", "")
        subject = params.get("subject", "Message from AI Assistant")
        body = params.get("body", "This message was sent by your AI assistant.")
        return self.messaging.send_email(recipient, subject, body)
    
    def make_call(self, params: Dict[str, Any]) -> str:
        phone_number = params.get("phone", "")
        return self.phone_integration.make_call(phone_number)
    
    def web_search(self, params: Dict[str, Any]) -> str:
        query = params.get("query", "")
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return self.web_controller.open_website(search_url)
    
    def delete_folder(self, params: Dict[str, Any]) -> str:
        folder_name = params.get("folder", "")
        if not folder_name:
            return "No folder name specified"
        
        folder_map = {
            "documents": os.path.expanduser("~/Documents"),
            "downloads": os.path.expanduser("~/Downloads"),
            "pictures": os.path.expanduser("~/Pictures"),
            "music": os.path.expanduser("~/Music"),
            "videos": os.path.expanduser("~/Videos")
        }
        
        if folder_name not in folder_map:
            return "Cannot delete system folders"
        
        folder_path = folder_map[folder_name]
        
        # Safety check - don't allow deleting actual system folders
        if folder_name in ["documents", "downloads", "pictures", "music", "videos"]:
            return f"Cannot delete the {folder_name} folder for security reasons"
        
        try:
            import shutil
            shutil.rmtree(folder_path)
            return f"Deleted folder: {folder_name}"
        except Exception as e:
            return f"Failed to delete folder: {str(e)}"
    
    def rename_file(self, params: Dict[str, Any]) -> str:
        # This would need more sophisticated parameter extraction
        return "Rename functionality not yet implemented"
    
    def rename_folder(self, params: Dict[str, Any]) -> str:
        # This would need more sophisticated parameter extraction
        return "Rename functionality not yet implemented"
    
    def take_screenshot(self, params: Dict[str, Any]) -> str:
        try:
            screenshots_dir = os.path.expanduser("~/Pictures/Screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            filename = params.get("filename", "screenshot.png")
            filepath = os.path.join(screenshots_dir, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"
    
    def open_browser(self, params: Dict[str, Any]) -> str:
        try:
            # Try to open Chrome first, then fall back to default browser
            chrome_path = self.config.get("application_paths", {}).get("chrome", "")
            if chrome_path and os.path.exists(chrome_path):
                subprocess.Popen(chrome_path)
                return "Opened Chrome browser"
            else:
                # Open default browser
                import webbrowser
                webbrowser.open_new("")
                return "Opened default browser"
        except Exception as e:
            return f"Failed to open browser: {str(e)}"
    
    def search_web(self, params: Dict[str, Any]) -> str:
        query = params.get("query", "")
        if not query:
            return "No search query specified"
        
        try:
            import webbrowser
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open_new(search_url)
            return f"Searching for: {query}"
        except Exception as e:
            return f"Failed to perform web search: {str(e)}"