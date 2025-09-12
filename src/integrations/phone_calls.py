import logging
import re
from typing import Dict, Any, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class PhoneCallIntegration:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.twilio_client = self.initialize_twilio()
        
    def initialize_twilio(self) -> Optional[Client]:
        """Initialize Twilio client if configured"""
        try:
            account_sid = self.config.get('twilio_account_sid', '')
            auth_token = self.config.get('twilio_auth_token', '')
            from_number = self.config.get('twilio_phone_number', '')
            
            if not all([account_sid, auth_token, from_number]):
                self.logger.warning("Twilio not configured. Phone calls will not work.")
                return None
            
            return Client(account_sid, auth_token)
        except Exception as e:
            self.logger.error(f"Failed to initialize Twilio: {str(e)}")
            return None
    
    def extract_phone_number(self, text: str) -> Tuple[str, str]:
        """Extract and validate phone number"""
        # Remove any non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', text)
        
        if not cleaned:
            return "", "No phone number provided"
        
        # Add country code if missing (assuming Ghana +233)
        if not cleaned.startswith('+'):
            if cleaned.startswith('0'):
                cleaned = '+233' + cleaned[1:]  # Ghana format
            else:
                cleaned = '+233' + cleaned  # Add Ghana code
        
        # Validate length
        if len(cleaned) < 10:
            return "", "Phone number too short"
        
        return cleaned, "success"
    
    def make_call_twilio(self, to_number: str, message: str = "") -> str:
        """Make phone call using Twilio"""
        if not self.twilio_client:
            return "Phone call service not configured. Please set up Twilio."
        
        try:
            from_number = self.config.get('twilio_phone_number', '')
            
            # Create call with text-to-speech message
            if message:
                call = self.twilio_client.calls.create(
                    twiml=f'<Response><Say>{message}</Say></Response>',
                    to=to_number,
                    from_=from_number
                )
            else:
                call = self.twilio_client.calls.create(
                    url='http://demo.twilio.com/docs/voice.xml',  # Default message
                    to=to_number,
                    from_=from_number
                )
            
            return f"Call initiated to {to_number}. Call SID: {call.sid}"
            
        except TwilioRestException as e:
            self.logger.error(f"Twilio error: {str(e)}")
            return f"Failed to make call: {str(e)}"
        except Exception as e:
            self.logger.error(f"Unexpected error making call: {str(e)}")
            return f"Failed to make call: {str(e)}"
    
    def make_call_skype(self, phone_number: str) -> str:
        """Make call using Skype (if installed)"""
        try:
            import subprocess
            import os
            
            # Skype URI scheme for calls
            skype_uri = f"skype:{phone_number}?call"
            
            if os.name == 'nt':  # Windows
                subprocess.Popen(f"start {skype_uri}", shell=True)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.Popen(["xdg-open", skype_uri])
            
            return f"Attempting to call {phone_number} via Skype"
            
        except Exception as e:
            self.logger.error(f"Skype call failed: {str(e)}")
            return f"Skype call failed: {str(e)}. Ensure Skype is installed."
    
    def make_call_android(self, phone_number: str) -> str:
        """Make call using ADB (requires connected Android device)"""
        try:
            import subprocess
            
            # Check if ADB is available
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if 'device' not in result.stdout:
                return "No Android device connected. Connect via USB and enable USB debugging."
            
            # Make call using ADB
            subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', f'tel:{phone_number}'])
            
            return f"Calling {phone_number} on connected Android device"
            
        except FileNotFoundError:
            return "ADB not found. Install Android Platform Tools."
        except Exception as e:
            self.logger.error(f"ADB call failed: {str(e)}")
            return f"Android call failed: {str(e)}"
    
    def make_call(self, phone_number: str, message: str = "") -> str:
        """Main method to make phone calls using available methods"""
        # Validate phone number
        phone, status = self.extract_phone_number(phone_number)
        if status != "success":
            return f"Error: {status}"
        
        # Try different methods in order of preference
        if self.twilio_client:
            return self.make_call_twilio(phone, message)
        else:
            # Fallback to other methods
            skype_result = self.make_call_skype(phone)
            if "failed" not in skype_result.lower():
                return skype_result
            
            android_result = self.make_call_android(phone)
            return android_result