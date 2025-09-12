import logging
import re
from typing import Dict, Any, Tuple
from src.utils.config import Config

class ModelHandler:
    def __init__(self, config: Config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.patterns = {
            "open_application": [
                r"open\s+(.+)$", 
                r"launch\s+(.+)$", 
                r"start\s+(.+)$"
            ],
            "open_folder": [
                r"open\s+(documents|downloads|pictures|music|videos|desktop|pics|pix|docs|download)",
                r"show\s+(my\s+)?(documents|downloads|pictures|music|videos|desktop)",
                r"open\s+(my\s+)?(documents|downloads|pictures|music|videos|desktop)",
                r"view\s+(documents|downloads|pictures|music|videos|desktop)",
                r"go to\s+(documents|downloads|pictures|music|videos|desktop)"
            ],
            "create_file": [
                r"create\s+(a\s+)?(file|document)",
                r"make\s+(a\s+)?(file|document)"
            ],
            "take_screenshot": [
                r"take\s+screenshot",
                r"capture\s+screen"
            ],
            "open_browser": [
                r"open\s+(browser|chrome|firefox|internet)"
            ],
            "search_web": [
                r"search\s+for\s+(.+)",
                r"google\s+(.+)",
                r"look\s+up\s+(.+)"
            ],
            "send_whatsapp": [
                r"send whatsapp (?:message|text) to (.+)",
                r"whatsapp (.+)",
                r"message (.+) on whatsapp",
                r"send message to (.+) on whatsapp"
            ],
            "send_email": [
                r"send email to (.+)",
                r"email (.+)",
                r"compose email to (.+)",
                r"send mail to (.+)"
            ],
            "send_message": [
                r"send message to (.+)",
                r"text (.+)",
                r"message (.+)"
            ],
            "make_phone_call": [
                r"call (.+)",
                r"phone call to (.+)",
                r"dial (.+)",
                r"ring (.+)",
                r"make call to (.+)",
                r"call number (.+)"
            ],
            "make_phone_call_with_message": [
                r"call (.+) and say (.+)",
                r"phone (.+) message (.+)",
                r"dial (.+) and tell them (.+)"
            ]
        }
        self.logger.info("Pattern-based model handler initialized")
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify user intent from text input using pattern matching"""
        try:
            if not text.strip():
                return "unknown", 0.0
            
            text_lower = text.lower()
            
            # Check each pattern
            for intent, patterns in self.patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, text_lower)
                    if match:
                        self.logger.debug(f"Intent matched: {intent} with pattern: {pattern}")
                        return intent, 0.8  # Fixed confidence for pattern matching
            
            # If no pattern matches, try keyword matching
            keywords = {
                "open_application": ["open", "launch", "start"],
                "open_folder": ["folder", "directory"],
                "create_file": ["create", "make", "new"],
                "take_screenshot": ["screenshot", "capture"],
                "open_browser": ["browser", "chrome", "firefox", "internet"],
                "search_web": ["search", "google", "look up"],
                "send_whatsapp": ["whatsapp", "message"],
                "send_email": ["email", "mail"],
                "send_message": ["message", "text", "contact"],
                "make_phone_call": ["call", "phone", "dial", "ring"]
            }
            
            for intent, words in keywords.items():
                if any(word in text_lower for word in words):
                    return intent, 0.6  # Lower confidence for keyword matching
            
            return "unknown", 0.0
            
        except Exception as e:
            self.logger.error(f"Error in intent classification: {str(e)}")
            return "unknown", 0.0
    
    def extract_parameters(self, text: str, intent: str) -> Dict[str, Any]:
        """Extract parameters from user text based on intent"""
        params = {}
        
        try:
            text_lower = text.lower()
            
            if intent == "open_application":
                # Extract application name
                for pattern in self.patterns["open_application"]:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        app_name = match.group(1).strip()
                        params["application"] = app_name
                        break
            
            elif intent == "open_folder":
                # Try to detect folder name with better pattern matching
                folders = ["documents", "downloads", "pictures", "music", "videos", "desktop", "pics", "pix", "docs", "download"]
                
                # Direct match
                for folder in folders:
                    if folder in text_lower:
                        params["folder"] = folder
                        break
                
                # Pattern matching
                if "folder" not in params:
                    folder_patterns = [
                        r"open\s+(documents|downloads|pictures|music|videos|desktop|pics|pix|docs|download)",
                        r"show\s+(my\s+)?(documents|downloads|pictures|music|videos|desktop)",
                        r"view\s+(documents|downloads|pictures|music|videos|desktop)"
                    ]
                    
                    for pattern in folder_patterns:
                        match = re.search(pattern, text_lower)
                        if match:
                            # Get the captured group (handle different pattern formats)
                            if match.lastindex >= 1:
                                folder_name = match.group(1) if match.group(1) else (match.group(2) if match.lastindex >= 2 else None)
                                if folder_name:
                                    params["folder"] = folder_name.lower()
                                    break
            
            elif intent == "search_web":
                # Extract search query
                for pattern in self.patterns["search_web"]:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        query = match.group(1).strip()
                        params["query"] = query
                        break
            
            elif intent == "send_whatsapp":
                # Extract phone number and message
                phone_patterns = [
                    r"to\s+([+\d\s]+)",
                    r"whatsapp\s+([+\d\s]+)",
                    r"message\s+([+\d\s]+)"
                ]
                
                for pattern in phone_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["phone"] = match.group(1).strip()
                        break
                
                # Extract message content
                message_patterns = [
                    r"message\s+(.+)",
                    r"say\s+(.+)",
                    r"text\s+(.+)"
                ]
                
                for pattern in message_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["message"] = match.group(1).strip()
                        break
                
                if "message" not in params:
                    params["message"] = "Hello from your AI assistant!"
            
            elif intent == "send_email":
                # Extract email address
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                match = re.search(email_pattern, text_lower)
                if match:
                    params["email"] = match.group(0)
                
                # Extract subject and body if mentioned
                subject_match = re.search(r"subject\s+(.+)", text_lower)
                if subject_match and subject_match.groups():
                    params["subject"] = subject_match.group(1).strip()
                
                body_match = re.search(r"body\s+(.+)", text_lower)
                if body_match and body_match.groups():
                    params["body"] = body_match.group(1).strip()
            
            elif intent == "send_message":
                # Generic message sending
                message_patterns = [
                    r"to\s+([+\d\s]+)",
                    r"message\s+([+\d\s]+)",
                    r"text\s+([+\d\s]+)"
                ]
                
                for pattern in message_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["recipient"] = match.group(1).strip()
                        break
                
                content_match = re.search(r"say\s+(.+)", text_lower)
                if content_match and content_match.groups():
                    params["message"] = content_match.group(1).strip()
            
            elif intent == "make_phone_call":
                # Extract phone number
                phone_patterns = [
                    r"to\s+([+\d\s]+)",
                    r"call\s+([+\d\s]+)",
                    r"phone\s+([+\d\s]+)",
                    r"dial\s+([+\d\s]+)"
                ]
                
                for pattern in phone_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["phone"] = match.group(1).strip()
                        break
            
            elif intent == "make_phone_call_with_message":
                # Extract phone number and message
                phone_patterns = [
                    r"call\s+([+\d\s]+)\s+and say",
                    r"phone\s+([+\d\s]+)\s+message",
                    r"dial\s+([+\d\s]+)\s+and tell them"
                ]
                
                for pattern in phone_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["phone"] = match.group(1).strip()
                        break
                
                # Extract message
                message_patterns = [
                    r"and say\s+(.+)",
                    r"message\s+(.+)",
                    r"and tell them\s+(.+)"
                ]
                
                for pattern in message_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["message"] = match.group(1).strip()
                        break
            
            return params
            
        except Exception as e:
            self.logger.error(f"Error extracting parameters: {str(e)}")
            return params