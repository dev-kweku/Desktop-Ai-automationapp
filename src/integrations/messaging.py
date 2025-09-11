import logging
import re
import pywhatkit
import yagmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Tuple
import time

class MessagingIntegration:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.email_config = self.load_email_config()
        
    def load_email_config(self) -> Dict[str, str]:
        """Load email configuration from config or environment variables"""
        return {
            'email': self.config.get('email_address', ''),
            'password': self.config.get('email_password', ''),
            'smtp_server': self.config.get('smtp_server', 'smtp.gmail.com'),
            'smtp_port': self.config.get('smtp_port', 587)
        }
    
    def extract_phone_number(self, text: str) -> Tuple[str, str]:
        """Extract phone number from text"""
        # Remove any non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', text)
        
        # Check if it's a valid phone number format
        if len(cleaned) >= 10:
            # Add country code if missing (assuming Ghana +233)
            if not cleaned.startswith('+'):
                if cleaned.startswith('0'):
                    cleaned = '+233' + cleaned[1:]  # Ghana format
                else:
                    cleaned = '+233' + cleaned  # Add Ghana code
            
            return cleaned, "success"
        
        return "", "No valid phone number found"
    
    def extract_email_address(self, text: str) -> Tuple[str, str]:
        """Extract email address from text"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        if match:
            return match.group(0), "success"
        return "", "No valid email address found"
    
    def send_whatsapp_message(self, phone_number: str, message: str) -> str:
        """Send WhatsApp message using pywhatkit"""
        try:
            # Validate phone number
            phone, status = self.extract_phone_number(phone_number)
            if status != "success":
                return f"Error: {status}"
            
            # Send message
            pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=True)
            return f"WhatsApp message sent successfully to {phone}"
            
        except Exception as e:
            self.logger.error(f"Failed to send WhatsApp message: {str(e)}")
            return f"Failed to send WhatsApp message: {str(e)}"
    
    def send_email_yagmail(self, recipient: str, subject: str, body: str) -> str:
        """Send email using yagmail (simpler method)"""
        try:
            if not self.email_config['email'] or not self.email_config['password']:
                return "Email configuration not set up. Please configure email settings."
            
            # Initialize yagmail
            yag = yagmail.SMTP(self.email_config['email'], self.email_config['password'])
            
            # Send email
            yag.send(
                to=recipient,
                subject=subject,
                contents=body
            )
            
            return f"Email sent successfully to {recipient}"
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return f"Failed to send email: {str(e)}"
    
    def send_email_smtp(self, recipient: str, subject: str, body: str) -> str:
        """Send email using SMTP (more control)"""
        try:
            if not self.email_config['email'] or not self.email_config['password']:
                return "Email configuration not set up. Please configure email settings."
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email']
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to server and send
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['email'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            return f"Email sent successfully to {recipient}"
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return f"Failed to send email: {str(e)}"
    
    def send_email(self, recipient: str, subject: str = "Message from AI Assistant", 
                body: str = "This message was sent by your AI assistant.") -> str:
        """Main email sending method"""
        # Validate email
        email, status = self.extract_email_address(recipient)
        if status != "success":
            return f"Error: {status}"
        
        # Try yagmail first, fall back to SMTP
        try:
            return self.send_email_yagmail(email, subject, body)
        except:
            return self.send_email_smtp(email, subject, body)
    
    def send_sms(self, phone_number: str, message: str) -> str:
        """Send SMS (placeholder for future implementation)"""
        # This would require integration with SMS APIs like Twilio
        return "SMS functionality not implemented yet. Would require SMS API integration."