import logging
import threading
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea,
                            QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDateTime
from PyQt5.QtGui import QFont
from src.nlp.intent_parser import IntentParser
from src.executor.action_executor import ActionExecutor
from src.voice.voice_manager import VoiceManager
from src.utils.config import Config
from .styles import get_stylesheet

class WorkerThread(QThread):
    """Thread for processing commands to keep GUI responsive"""
    finished = pyqtSignal(str, str)  # intent, result
    
    def __init__(self, intent_parser, action_executor, command):
        super().__init__()
        self.intent_parser = intent_parser
        self.action_executor = action_executor
        self.command = command
    
    def run(self):
        try:
            # Parse the command
            intent_data = self.intent_parser.parse_command(self.command)
            intent = intent_data.get("intent", "unknown")
            
            # Execute the action
            result = self.action_executor.execute(intent_data)
            
            self.finished.emit(intent, result)
        except Exception as e:
            self.finished.emit("error", f"Error processing command: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self, model_handler, action_executor, config):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.model_handler = model_handler
        self.action_executor = action_executor
        self.config = config
        self.intent_parser = IntentParser(model_handler)
        self.voice_manager = VoiceManager(config)
        
        # Connect voice signals
        self.voice_manager.voice_command_received.connect(self.handle_voice_command)
        self.voice_manager.listening_state_changed.connect(self.update_listening_ui)
        self.voice_manager.error_occurred.connect(self.handle_voice_error)
        
        self.setup_ui()
        self.setWindowTitle("Desktop AI Assistant with Voice")
        self.resize(900, 700)
    
    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Desktop AI Assistant with Voice Control")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Voice control group
        voice_group = QGroupBox("Voice Control")
        voice_layout = QVBoxLayout()
        
        # Voice buttons
        voice_btn_layout = QHBoxLayout()
        
        self.voice_toggle_btn = QPushButton("Start Listening")
        self.voice_toggle_btn.clicked.connect(self.toggle_voice_listening)
        voice_btn_layout.addWidget(self.voice_toggle_btn)
        
        self.voice_command_btn = QPushButton("Speak Command")
        self.voice_command_btn.clicked.connect(self.single_voice_command)
        voice_btn_layout.addWidget(self.voice_command_btn)
        
        self.speak_btn = QPushButton("Speak Response")
        self.speak_btn.clicked.connect(self.speak_last_response)
        voice_btn_layout.addWidget(self.speak_btn)
        
        voice_layout.addLayout(voice_btn_layout)
        
        # Voice status
        self.voice_status = QLabel("Voice: Ready")
        voice_layout.addWidget(self.voice_status)
        
        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)
        
        # Log output area
        log_label = QLabel("Activity Log:")
        log_label.setFont(QFont("Arial", 10))
        layout.addWidget(log_label)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(300)
        layout.addWidget(self.log_output)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your command or use voice...")
        self.input_field.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.input_field)
        
        self.run_button = QPushButton("Run Command")
        self.run_button.clicked.connect(self.execute_command)
        input_layout.addWidget(self.run_button)
        
        layout.addLayout(input_layout)
        
        # Button area
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("Clear Log")
        self.clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_button)
        
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Apply styles
        self.setStyleSheet(get_stylesheet())
        
        # Add initial message
        self.add_to_log("System", "Desktop AI Assistant with Voice initialized.")
        self.add_to_log("System", "Click 'Speak Command' to use voice input.")
    
    def toggle_voice_listening(self):
        """Toggle continuous voice listening"""
        is_listening = self.voice_manager.toggle_listening()
        if is_listening:
            self.voice_toggle_btn.setText("Stop Listening")
            self.add_to_log("System", "Continuous listening started. Say your commands.")
            self.voice_manager.speak("Continuous listening started. I'm ready for your commands.")
        else:
            self.voice_toggle_btn.setText("Start Listening")
            self.add_to_log("System", "Continuous listening stopped.")
            self.voice_manager.speak("Listening stopped.")
    
    def single_voice_command(self):
        """Listen for a single voice command"""
        def listen_thread():
            command = self.voice_manager.listen()
            if command:
                self.handle_voice_command(command)
        
        thread = threading.Thread(target=listen_thread)
        thread.daemon = True
        thread.start()
    
    def handle_voice_command(self, command):
        """Process voice command received"""
        self.add_to_log("Voice", command)
        self.input_field.setText(command)
        self.execute_command()
    
    def speak_last_response(self):
        """Speak the last response from the assistant"""
        # Get the last response from log
        log_text = self.log_output.toPlainText()
        lines = log_text.split('\n')
        for line in reversed(lines):
            if "Assistant:" in line:
                response = line.split("Assistant:")[1].strip()
                self.voice_manager.speak(response)
                break
        else:
            self.voice_manager.speak("No response found to speak.")
    
    def update_listening_ui(self, is_listening):
        """Update UI based on listening state"""
        if is_listening:
            self.voice_status.setText("Voice: Listening...")
            self.voice_status.setStyleSheet("color: blue; font-weight: bold;")
        else:
            self.voice_status.setText("Voice: Ready")
            self.voice_status.setStyleSheet("color: black;")
    
    def handle_voice_error(self, error_message):
        """Handle voice-related errors"""
        self.add_to_log("Error", error_message)
        self.voice_status.setText(f"Voice Error: {error_message}")
        self.voice_status.setStyleSheet("color: red; font-weight: bold;")
    
    def execute_command(self):
        command = self.input_field.text().strip()
        if not command:
            return
        
        # Clear input field
        self.input_field.clear()
        
        # Add command to log
        self.add_to_log("User", command)
        self.status_label.setText("Processing command...")
        
        # Disable buttons while processing
        self.run_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.voice_command_btn.setEnabled(False)
        self.voice_toggle_btn.setEnabled(False)
        self.speak_btn.setEnabled(False)
        
        # Create and start worker thread
        self.worker = WorkerThread(self.intent_parser, self.action_executor, command)
        self.worker.finished.connect(self.on_command_finished)
        self.worker.start()
    
    def on_command_finished(self, intent, result):
        # Re-enable buttons
        self.run_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.voice_command_btn.setEnabled(True)
        self.voice_toggle_btn.setEnabled(True)
        self.speak_btn.setEnabled(True)
        
        # Add result to log
        self.add_to_log("Assistant", result)
        self.status_label.setText("Ready")
        
        # Speak the result if it's not too long
        if len(result) < 100:  # Don't speak very long responses
            self.voice_manager.speak(result)
    
    def add_to_log(self, sender, message):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        formatted_message = f"[{timestamp}] {sender}: {message}"
        self.log_output.append(formatted_message)
        
        # Auto-scroll to bottom
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )
    
    def clear_log(self):
        self.log_output.clear()
        self.add_to_log("System", "Log cleared")
    
    def closeEvent(self, event):
        self.logger.info("Application closing")
        # Stop voice listening if active
        if hasattr(self.voice_manager, 'stop_continuous_listening'):
            self.voice_manager.stop_continuous_listening()
        event.accept()