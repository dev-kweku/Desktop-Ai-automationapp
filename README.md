# Desktop AI Assistant - Comprehensive Documentation

## 📖 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [Features](#features)
7. [Development Guide](#development-guide)
8. [Troubleshooting](#troubleshooting)
9. [API Reference](#api-reference)
10. [Future Enhancements](#future-enhancements)

## 🚀 Project Overview

**Desktop AI Assistant** is a comprehensive artificial intelligence application that enables users to control their computer and perform various tasks using natural language commands and voice control. The application bridges the gap between human-computer interaction by providing seamless desktop automation with AI capabilities.

### Key Objectives
- Provide natural language command processing
- Enable voice-controlled desktop operations
- Offer cross-platform messaging capabilities
- Automate routine computer tasks
- Enhance productivity through AI assistance

### Technology Stack
- **Frontend**: PyQt5 for GUI
- **Backend**: Python 3.8+
- **AI/NLP**: Pattern-based intent recognition (with Hugging Face integration capability)
- **Voice**: SpeechRecognition + pyttsx3
- **Messaging**: pywhatkit + SMTP integration

## 🏗️ Architecture

### System Architecture
```
Desktop AI Assistant
├── GUI Layer (PyQt5)
├── NLP Layer (Intent Processing)
├── Execution Layer (Action Handling)
├── Integration Layer (External Services)
└── Utilities (Config, Logging, Security)
```

### Module Structure
```
src/
├── gui/              # User interface components
├── nlp/             # Natural language processing
├── executor/        # Command execution
├── integrations/    # External service integrations
├── voice/           # Voice input/output
├── utils/           # Utilities and helpers
└── tests/           # Test cases
```

### Data Flow
1. User input (text/voice) → GUI Layer
2. Input processing → NLP Layer
3. Intent recognition → Execution Layer
4. Action execution → Integration Layer
5. Response generation → GUI Layer

## 📦 Installation Guide

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 or macOS/Linux
- Internet connection (for some features)
- Microphone (for voice commands)

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd desktop-ai-assistant
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements_voice.txt
   ```

4. **Optional: Install Additional Dependencies**
   ```bash
   # For advanced AI capabilities
   pip install transformers torch
   ```

5. **Run the Application**
   ```bash
   python src/main.py
   ```

## ⚙️ Configuration

### Configuration File (config.json)

```json
{
    "model_name": "pattern_based",
    "log_level": "INFO",
    "allowed_directories": [
        "~/Documents",
        "~/Downloads",
        "~/Pictures"
    ],
    "application_paths": {
        "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "notepad": "C:/Windows/System32/notepad.exe"
    },
    "email_address": "your_email@gmail.com",
    "email_password": "your_app_password",
    "messaging_settings": {
        "whatsapp_wait_time": 15,
        "close_browser_after_send": true
    }
}
```

### Email Setup

1. **Gmail Configuration:**
   - Enable 2-factor authentication
   - Generate app password:
     - Go to Google Account → Security → 2-Step Verification → App passwords
     - Generate password for "Mail"
     - Use this password in config.json

2. **Other Email Providers:**
   - Update SMTP server and port settings
   - Example for Outlook: `"smtp_server": "smtp.office365.com", "smtp_port": 587`

### WhatsApp Setup
- Ensure WhatsApp Web is logged in Chrome
- Keep browser open for message sending
- Use international phone format: +233123456789

## 🎯 Usage Guide

### Basic Commands

**File Operations:**
- "Open documents folder"
- "Create a new file"
- "Take a screenshot"

**Application Control:**
- "Open Chrome browser"
- "Start calculator"
- "Launch notepad"

**System Operations:**
- "Show me downloads"
- "Open pictures"
- "Play music"

### Messaging Commands

**WhatsApp Messages:**
- "Send WhatsApp message to +233123456789"
- "WhatsApp John say hello"
- "Text +233123456789 on WhatsApp"

**Email Commands:**
- "Send email to example@gmail.com"
- "Email boss subject Report body Please find attached"
- "Compose mail to client@company.com"

**Generic Messages:**
- "Message +233123456789"
- "Contact example@gmail.com"

### Voice Commands
- Click "Speak Command" and speak naturally
- "Start Listening" for continuous voice mode
- "Speak Response" to hear last response

### Advanced Usage

**Scheduled Messages:**
- "Schedule message to +233123456789 for tomorrow"
- "Plan WhatsApp message for later"

**Custom Commands:**
- Add patterns in `src/nlp/model_handler.py`
- Extend executor with new functions

## ✨ Features

### Core Features
- ✅ Natural Language Processing
- ✅ Voice Recognition & Synthesis
- ✅ Desktop Automation
- ✅ File Operations
- ✅ Application Control
- ✅ Cross-platform Messaging
- ✅ Scheduled Tasks
- ✅ Security Management

### Messaging Capabilities
- **WhatsApp Integration**: Send instant messages
- **Email Integration**: SMTP-based email sending
- **SMS Ready**: Framework for future SMS integration
- **Multi-format Support**: Phone numbers and emails

### Voice Features
- **Speech-to-Text**: Convert spoken commands to text
- **Text-to-Speech**: Read responses aloud
- **Continuous Listening**: Background voice monitoring
- **Noise Cancellation**: Ambient noise adjustment

### Security Features
- **Safe Directory Access**: Restricted file operations
- **Command Validation**: Prevents dangerous operations
- **Email Encryption**: Secure SMTP connections
- **Privacy Focused**: Local processing where possible

## 🛠️ Development Guide

### Adding New Commands

1. **Add NLP Patterns** (`src/nlp/model_handler.py`):
   ```python
   "new_command": [
       r"pattern one (.+)",
       r"pattern two (.+)"
   ]
   ```

2. **Add Execution Method** (`src/executor/action_executor.py`):
   ```python
   def new_command(self, params: Dict[str, Any]) -> str:
       # Implementation here
       return "Success message"
   ```

3. **Update Execute Method**:
   ```python
   elif intent == "new_command":
       return self.new_command(params)
   ```

### Extending Integrations

**New Service Integration:**
1. Create module in `src/integrations/`
2. Implement service class
3. Add to executor initialization
4. Update configuration if needed

### Testing

**Run Tests:**
```bash
python -m pytest tests/ -v
```

**Test Specific Features:**
```bash
# Test messaging
python tests/test_messaging.py

# Test voice
python tests/test_voice.py
```

## 🐛 Troubleshooting

### Common Issues

**Voice Recognition Not Working:**
- Check microphone permissions
- Run microphone setup in system settings
- Ensure PyAudio is properly installed

**WhatsApp Messages Fail:**
- Verify WhatsApp Web is logged in
- Check internet connection
- Ensure Chrome is default browser

**Email Sending Fails:**
- Verify app password (not regular password)
- Check SMTP settings
- Test email configuration:
  ```bash
  python src/utils/setup_config.py
  ```

**Application Crashes:**
- Check log files in `logs/app.log`
- Verify all dependencies are installed
- Ensure sufficient system resources

### Debug Mode

Enable debug logging in `config.json`:
```json
{
    "log_level": "DEBUG",
    "log_file": "./logs/debug.log"
}
```

### Performance Optimization

- Close unused applications during voice recognition
- Use wired internet for messaging features
- Ensure sufficient RAM (4GB+ recommended)

## 📚 API Reference

### Core Classes

**VoiceManager** (`src/voice/voice_manager.py`)
- `speak(text)`: Convert text to speech
- `listen()`: Capture voice input
- `toggle_listening()`: Control continuous listening

**MessagingIntegration** (`src/integrations/messaging.py`)
- `send_whatsapp_message(phone, message)`: Send WhatsApp
- `send_email(recipient, subject, body)`: Send email
- `extract_contact_info(text)`: Parse contact details

**ActionExecutor** (`src/executor/action_executor.py`)
- `execute(intent_data)`: Main execution method
- Various action methods for different intents

### Utility Functions

**Config Management** (`src/utils/config.py`)
- `load_config()`: Load configuration
- `get(key, default)`: Get config value
- `save_config(new_config)`: Update configuration

**Security** (`src/utils/security.py`)
- `is_safe_path(path)`: Validate file access
- `is_dangerous_command(command)`: Check command safety

## 🔮 Future Enhancements

### Short-term Goals
- [ ] Mobile app companion
- [ ] Calendar integration
- [ ] Weather information
- [ ] News updates
- [ ] Multi-language support

### Medium-term Goals
- [ ] Advanced AI model integration
- [ ] Cross-device synchronization
- [ ] Plugin system
- [ ] Cloud backup
- [ ] API endpoints

### Long-term Vision
- [ ] IoT device control
- [ ] Smart home integration
- [ ] Predictive assistance
- [ ] Machine learning customization
- [ ] Enterprise features

## 🤝 Contributing

### Development Process
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

