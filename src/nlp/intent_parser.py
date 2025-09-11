import logging
from typing import Dict, Any
from .model_handler import ModelHandler

class IntentParser:
    def __init__(self, model_handler: ModelHandler):
        self.logger = logging.getLogger(__name__)
        self.model_handler = model_handler
    
    def parse_command(self, text: str) -> Dict[str, Any]:
        """Parse user command and return structured intent with parameters"""
        try:
            # Classify intent
            intent, confidence = self.model_handler.classify_intent(text)
            
            # Extract parameters based on intent
            parameters = self.model_handler.extract_parameters(text, intent)
            
            result = {
                "intent": intent,
                "confidence": confidence,
                "parameters": parameters,
                "original_text": text
            }
            
            self.logger.info(f"Parsed command: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error parsing command: {str(e)}")
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "parameters": {},
                "original_text": text
            }