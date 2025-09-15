import logging
import re
from typing import Dict, Any, Tuple
from src.utils.config import Config

class ModelHandler:
    def __init__(self, config: Config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Reordered patterns: specific intents first, then general ones
        self.patterns = {
            "open_folder": [
                r"open\s+(documents|document|docs|doc|downloads|download|pictures|picture|pics|pix|photos|images|photo|image|music|videos|video|desktop|desk)",
                r"show\s+(my\s+)?(documents|document|docs|doc|downloads|download|pictures|picture|pics|pix|photos|images|photo|image|music|videos|video|desktop|desk)",
                r"view\s+(documents|document|docs|doc|downloads|download|pictures|picture|pics|pix|photos|images|photo|image|music|videos|video|desktop|desk)",
                r"go to\s+(documents|document|docs|doc|downloads|download|pictures|picture|pics|pix|photos|images|photo|image|music|videos|video|desktop|desk)",
                r"open\s+my\s+(documents|document|docs|doc|downloads|download|pictures|picture|pics|pix|photos|images|photo|image|music|videos|video|desktop|desk)",
                r"open\s+the\s+(documents|document|docs|doc|downloads|download|pictures|picture|pics|pix|photos|images|photo|image|music|videos|video|desktop|desk)",
                r"open\s+(\w+)\s*(folder|directory)",
                r"show\s+me\s+the\s+(\w+)\s*(folder|directory)"
            ],
            "open_application": [
                r"open\s+(.+)$", 
                r"launch\s+(.+)$", 
                r"start\s+(.+)$",
                r"run\s+(.+)$"
            ],
            "create_file": [
                r"create\s+(a\s+)?(file|document)",
                r"make\s+(a\s+)?(file|document)",
                r"new\s+(file|document)"
            ],
            "take_screenshot": [
                r"take\s+screenshot",
                r"capture\s+screen",
                r"screenshot",
                r"take\s+screen\s+shot"
            ],
            "open_browser": [
                r"open\s+(browser|chrome|firefox|edge|safari|internet|web)",
                r"launch\s+(browser|chrome|firefox|edge|safari|internet|web)",
                r"start\s+(browser|chrome|firefox|edge|safari|internet|web)"
            ],
            "search_web": [
                r"search\s+for\s+(.+)",
                r"google\s+(.+)",
                r"look\s+up\s+(.+)",
                r"find\s+(.+)",
                r"search\s+(.+)"
            ],
            "send_whatsapp": [
                r"send\s+whatsapp\s+(?:message|text)\s+to\s+(.+)",
                r"whatsapp\s+(.+)",
                r"message\s+(.+)\s+on\s+whatsapp",
                r"send\s+message\s+to\s+(.+)\s+on\s+whatsapp",
                r"text\s+(.+)\s+on\s+whatsapp"
            ],
            "send_email": [
                r"send\s+email\s+to\s+(.+)",
                r"email\s+(.+)",
                r"compose\s+email\s+to\s+(.+)",
                r"send\s+mail\s+to\s+(.+)",
                r"write\s+email\s+to\s+(.+)"
            ],
            "send_message": [
                r"send\s+message\s+to\s+(.+)",
                r"text\s+(.+)",
                r"message\s+(.+)",
                r"contact\s+(.+)"
            ],
            "make_phone_call": [
                r"call\s+(.+)",
                r"phone\s+call\s+to\s+(.+)",
                r"dial\s+(.+)",
                r"ring\s+(.+)",
                r"make\s+call\s+to\s+(.+)",
                r"call\s+number\s+(.+)"
            ],
            "make_phone_call_with_message": [
                r"call\s+(.+)\s+and\s+say\s+(.+)",
                r"phone\s+(.+)\s+message\s+(.+)",
                r"dial\s+(.+)\s+and\s+tell\s+them\s+(.+)",
                r"call\s+(.+)\s+and\s+tell\s+them\s+(.+)"
            ]
        }
        self.logger.info("Pattern-based model handler initialized")
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify user intent from text input using pattern matching"""
        try:
            if not text.strip():
                return "unknown", 0.0
            
            text_lower = text.lower()
            self.logger.debug(f"Classifying text: '{text_lower}'")
            
            # Check each pattern in order (specific patterns first)
            for intent, patterns in self.patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, text_lower)
                    if match:
                        self.logger.debug(f"Intent matched: {intent} with pattern: {pattern}")
                        self.logger.debug(f"Match groups: {match.groups()}")
                        return intent, 0.8  # Fixed confidence for pattern matching
            
            # If no pattern matches, try keyword matching
            keywords = {
                "open_application": ["open", "launch", "start", "run", "app", "application", "program", "software"],
                "open_folder": ["folder", "directory", "documents", "document", "downloads", "download", "pictures", "picture", 
                                "music", "videos", "video", "desktop", "photos", "images", "docs", "pics", "pix"],
                "create_file": ["create", "make", "new", "file", "document"],
                "take_screenshot": ["screenshot", "capture", "screen", "shot"],
                "open_browser": ["browser", "chrome", "firefox", "edge", "safari", "internet", "web"],
                "search_web": ["search", "google", "look up", "find", "query"],
                "send_whatsapp": ["whatsapp", "message", "text", "send", "whats app"],
                "send_email": ["email", "mail", "send email", "compose", "gmail"],
                "send_message": ["message", "text", "contact", "reach", "sms"],
                "make_phone_call": ["call", "phone", "dial", "ring", "contact", "number"]
            }
            
            for intent, words in keywords.items():
                if any(word in text_lower for word in words):
                    self.logger.debug(f"Intent matched by keywords: {intent}")
                    return intent, 0.6  # Lower confidence for keyword matching
            
            self.logger.debug("No intent matched, returning 'unknown'")
            return "unknown", 0.0
            
        except Exception as e:
            self.logger.error(f"Error in intent classification: {str(e)}")
            return "unknown", 0.0
    
    def extract_parameters(self, text: str, intent: str) -> Dict[str, Any]:
        """Extract parameters from user text based on intent"""
        params = {}
        
        try:
            text_lower = text.lower()
            self.logger.debug(f"Extracting parameters for intent '{intent}' from text: '{text_lower}'")
            
            if intent == "open_application":
                # Extract application name - more flexible approach
                app_patterns = [
                    r"open\s+(.+)",
                    r"launch\s+(.+)",
                    r"start\s+(.+)",
                    r"run\s+(.+)"
                ]
                
                for pattern in app_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        app_name = match.group(1).strip()
                        # Remove common filler words
                        app_name = re.sub(r'\b(the|my|a|an)\b', '', app_name).strip()
                        params["application"] = app_name
                        self.logger.debug(f"Extracted application: {app_name}")
                        break
            
            elif intent == "open_folder":
                # List of supported folders with variations
                folder_mappings = {
                    "documents": ["documents", "docs", "document", "doc"],
                    "downloads": ["downloads", "download"],
                    "pictures": ["pictures", "pics", "picture", "photos", "images", "photo", "image"],
                    "music": ["music", "songs", "tunes"],
                    "videos": ["videos", "video", "movies", "films"],
                    "desktop": ["desktop", "desk"]
                }
                
                # Check for exact matches first
                for folder_name, variations in folder_mappings.items():
                    for variation in variations:
                        if variation in text_lower:
                            params["folder"] = folder_name
                            self.logger.debug(f"Exact folder match: {folder_name}")
                            break
                    if "folder" in params:
                        break
                
                # If no exact match, try pattern matching
                if "folder" not in params:
                    folder_patterns = [
                        r"open\s+(\w+)\s*(folder|directory)",
                        r"show\s+me\s+the\s+(\w+)\s*(folder|directory)",
                        r"go to\s+my\s+(\w+)\s*(folder|directory)"
                    ]
                    
                    for pattern in folder_patterns:
                        match = re.search(pattern, text_lower)
                        if match and match.groups():
                            potential_folder = match.group(1).lower()
                            # Map to standard folder names
                            for folder_name, variations in folder_mappings.items():
                                if potential_folder in variations:
                                    params["folder"] = folder_name
                                    self.logger.debug(f"Pattern folder match: {folder_name}")
                                    break
                            if "folder" in params:
                                break
                
                # Final fallback: use the word after "open" if it's a known folder
                if "folder" not in params:
                    open_match = re.search(r"open\s+(\w+)", text_lower)
                    if open_match and open_match.group(1):
                        potential_folder = open_match.group(1).lower()
                        # Check if this is a common folder name
                        common_folders = ["documents", "document", "downloads", "download", "pictures", "picture", 
                                         "music", "videos", "video", "desktop"]
                        if potential_folder in common_folders:
                            params["folder"] = potential_folder
                            self.logger.debug(f"Fallback folder match: {potential_folder}")
            
            elif intent == "search_web":
                # Extract search query
                for pattern in self.patterns["search_web"]:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        query = match.group(1).strip()
                        params["query"] = query
                        self.logger.debug(f"Extracted search query: {query}")
                        break
            
            elif intent == "send_whatsapp":
                # Extract phone number and message
                phone_patterns = [
                    r"to\s+([+\d\s]+)",
                    r"whatsapp\s+([+\d\s]+)",
                    r"message\s+([+\d\s]+)",
                    r"text\s+([+\d\s]+)",
                    r"send\s+to\s+([+\d\s]+)"
                ]
                
                for pattern in phone_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["phone"] = match.group(1).strip()
                        self.logger.debug(f"Extracted phone: {params['phone']}")
                        break
                
                # Extract message content
                message_patterns = [
                    r"message\s+(.+)",
                    r"say\s+(.+)",
                    r"text\s+(.+)",
                    r"that\s+(.+)",
                    r"with\s+message\s+(.+)"
                ]
                
                for pattern in message_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["message"] = match.group(1).strip()
                        self.logger.debug(f"Extracted message: {params['message']}")
                        break
                
                if "message" not in params:
                    params["message"] = "Hello from your AI assistant!"
                    self.logger.debug("Using default message")
            
            elif intent == "send_email":
                # Extract email address
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                match = re.search(email_pattern, text_lower)
                if match:
                    params["email"] = match.group(0)
                    self.logger.debug(f"Extracted email: {params['email']}")
                
                # Extract subject and body if mentioned
                subject_match = re.search(r"subject\s+(.+)", text_lower)
                if subject_match and subject_match.groups():
                    params["subject"] = subject_match.group(1).strip()
                    self.logger.debug(f"Extracted subject: {params['subject']}")
                
                body_match = re.search(r"body\s+(.+)", text_lower)
                if body_match and body_match.groups():
                    params["body"] = body_match.group(1).strip()
                    self.logger.debug(f"Extracted body: {params['body']}")
            
            elif intent == "send_message":
                # Generic message sending
                message_patterns = [
                    r"to\s+([+\d\s]+)",
                    r"message\s+([+\d\s]+)",
                    r"text\s+([+\d\s]+)",
                    r"contact\s+([+\d\s]+)"
                ]
                
                for pattern in message_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["recipient"] = match.group(1).strip()
                        self.logger.debug(f"Extracted recipient: {params['recipient']}")
                        break
                
                content_match = re.search(r"say\s+(.+)", text_lower)
                if content_match and content_match.groups():
                    params["message"] = content_match.group(1).strip()
                    self.logger.debug(f"Extracted message: {params['message']}")
            
            elif intent == "make_phone_call":
                # Extract phone number
                phone_patterns = [
                    r"to\s+([+\d\s]+)",
                    r"call\s+([+\d\s]+)",
                    r"phone\s+([+\d\s]+)",
                    r"dial\s+([+\d\s]+)",
                    r"number\s+([+\d\s]+)"
                ]
                
                for pattern in phone_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["phone"] = match.group(1).strip()
                        self.logger.debug(f"Extracted phone: {params['phone']}")
                        break
            
            elif intent == "make_phone_call_with_message":
                # Extract phone number and message
                phone_patterns = [
                    r"call\s+([+\d\s]+)\s+and say",
                    r"phone\s+([+\d\s]+)\s+message",
                    r"dial\s+([+\d\s]+)\s+and tell them",
                    r"call\s+([+\d\s]+)\s+and tell them"
                ]
                
                for pattern in phone_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["phone"] = match.group(1).strip()
                        self.logger.debug(f"Extracted phone: {params['phone']}")
                        break
                
                # Extract message
                message_patterns = [
                    r"and say\s+(.+)",
                    r"message\s+(.+)",
                    r"and tell them\s+(.+)",
                    r"tell them\s+(.+)"
                ]
                
                for pattern in message_patterns:
                    match = re.search(pattern, text_lower)
                    if match and match.groups():
                        params["message"] = match.group(1).strip()
                        self.logger.debug(f"Extracted message: {params['message']}")
                        break
            
            self.logger.debug(f"Final parameters: {params}")
            return params
            
        except Exception as e:
            self.logger.error(f"Error extracting parameters: {str(e)}")
            return params