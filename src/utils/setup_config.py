import json
import os
import getpass

def setup_email_config():
    """Interactive email configuration setup"""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
    
    if not os.path.exists(config_path):
        print("Config file not found. Please run the application first to generate it.")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("=== Email Configuration Setup ===")
    print("This will help you set up email functionality for your AI assistant.")
    print()
    
    email = input("Enter your email address: ").strip()
    password = getpass.getpass("Enter your email app password (will be hidden): ").strip()
    
    if email and password:
        config['email_address'] = email
        config['email_password'] = password
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        print("Email configuration saved successfully!")
        print("You can now use email commands with your AI assistant.")
    else:
        print("Configuration cancelled.")

if __name__ == "__main__":
    setup_email_config()