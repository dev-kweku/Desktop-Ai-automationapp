import threading
import speech_recognition as sr
import pyttsx3
import logging
from queue import Queue
from PyQt5.QtCore import pyqtSignal, QObject

class VoiceManager(QObject):
    """Manages voice input and output functionality"""
    
    # Signals for GUI updates
    voice_command_received = pyqtSignal(str)
    listening_state_changed = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.command_queue = Queue()
        self.is_listening = False
        self.stop_listening = False
        
        # Configure TTS engine
        self.setup_tts()
        
        # Adjust for ambient noise
        try:
            self.logger.info("Adjusting for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.logger.info("Voice manager initialized")
        except Exception as e:
            self.logger.error(f"Error adjusting for ambient noise: {str(e)}")
            self.error_occurred.emit(f"Microphone error: {str(e)}")
    
    def setup_tts(self):
        """Configure text-to-speech engine"""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)  # Use first available voice
            self.tts_engine.setProperty('rate', 150)  # Speed percent
            self.tts_engine.setProperty('volume', 0.9)  # Volume 0-1
        except Exception as e:
            self.logger.error(f"Error setting up TTS: {str(e)}")
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            def speak_thread():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            # Run in separate thread to avoid blocking GUI
            thread = threading.Thread(target=speak_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.logger.error(f"Error in text-to-speech: {str(e)}")
            self.error_occurred.emit(f"TTS Error: {str(e)}")
    
    def listen(self):
        """Listen for voice command and return transcribed text"""
        try:
            self.listening_state_changed.emit(True)
            
            with self.microphone as source:
                self.logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            self.logger.info("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            self.logger.info(f"Recognized: {text}")
            
            self.listening_state_changed.emit(False)
            return text.lower()
            
        except sr.WaitTimeoutError:
            self.listening_state_changed.emit(False)
            self.logger.warning("Listening timeout")
            return None
        except sr.UnknownValueError:
            self.listening_state_changed.emit(False)
            self.logger.warning("Could not understand audio")
            self.speak("Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError as e:
            self.listening_state_changed.emit(False)
            self.logger.error(f"Speech recognition error: {str(e)}")
            self.error_occurred.emit("Speech recognition service error")
            return None
        except Exception as e:
            self.listening_state_changed.emit(False)
            self.logger.error(f"Unexpected error in listen: {str(e)}")
            return None
    
    def start_continuous_listening(self):
        """Start continuous listening in background thread"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.stop_listening = False
        
        def listening_loop():
            while self.is_listening and not self.stop_listening:
                try:
                    command = self.listen()
                    if command:
                        self.voice_command_received.emit(command)
                        self.speak(f"Got it. Executing {command}")
                    # Short pause before listening again
                    threading.Event().wait(2)
                except Exception as e:
                    self.logger.error(f"Error in listening loop: {str(e)}")
                    break
            
            self.is_listening = False
            self.listening_state_changed.emit(False)
        
        thread = threading.Thread(target=listening_loop)
        thread.daemon = True
        thread.start()
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.stop_listening = True
        self.is_listening = False
    
    def toggle_listening(self):
        """Toggle continuous listening state"""
        if self.is_listening:
            self.stop_continuous_listening()
            return False
        else:
            self.start_continuous_listening()
            return True