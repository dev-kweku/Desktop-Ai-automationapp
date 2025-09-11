import os
import logging
from src.utils.config import Config

class SecurityManager:
    def __init__(self, config: Config):
        self.logger = logging.getLogger(__name__)
        self.config = config
    
    def is_safe_path(self, path: str) -> bool:
        """Check if a path is safe to access (within allowed directories)"""
        try:
            # Resolve the absolute path
            abs_path = os.path.abspath(os.path.expanduser(path))
            
            # Check if the path is within any allowed directory
            allowed_dirs = [os.path.abspath(os.path.expanduser(d)) 
                        for d in self.config.get("allowed_directories", [])]
            
            for allowed_dir in allowed_dirs:
                if abs_path.startswith(allowed_dir):
                    return True
            
            self.logger.warning(f"Blocked access to restricted path: {abs_path}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking path safety: {str(e)}")
            return False
    
    def is_dangerous_command(self, command: str) -> bool:
        """Check if a command contains dangerous patterns"""
        dangerous_patterns = self.config.get("dangerous_commands", [])
        command_lower = command.lower()
        
        for pattern in dangerous_patterns:
            if pattern in command_lower:
                self.logger.warning(f"Blocked dangerous command: {command}")
                return True
        
        return False