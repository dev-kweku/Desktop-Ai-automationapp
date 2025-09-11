import sys
import os
import logging

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.gui.main_window import MainWindow
from src.nlp.model_handler import ModelHandler
from src.executor.action_executor import ActionExecutor
from src.utils.logger import setup_logging
from src.utils.config import Config
from PyQt5.QtWidgets import QApplication

def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = Config()
        
        # Initialize application
        app = QApplication(sys.argv)
        
        # Initialize components
        model_handler = ModelHandler(config)
        action_executor = ActionExecutor(config)
        
        # Create and show main window
        window = MainWindow(model_handler, action_executor, config)
        window.show()
        
        logger.info("Desktop AI Assistant with Voice started successfully")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()