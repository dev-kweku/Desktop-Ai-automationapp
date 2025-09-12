# import sys
# import os
# import logging
# import traceback


# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# def main():

#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         handlers=[
#             logging.FileHandler('./logs/app.log'),
#             logging.StreamHandler()
#         ]
#     )
    
#     logger = logging.getLogger(__name__)
    
#     try:
        
#         from src.gui.main_window import MainWindow
#         from src.nlp.model_handler import ModelHandler
#         from src.executor.action_executor import ActionExecutor
#         from src.utils.logger import setup_logging
#         from src.utils.config import Config
#         from PyQt5.QtWidgets import QApplication
        
        
#         setup_logging()
        
        
#         config = Config()
        
        
#         app = QApplication(sys.argv)
        
        
#         model_handler = ModelHandler(config)
#         action_executor = ActionExecutor(config)
        
        
#         window = MainWindow(model_handler, action_executor, config)
#         window.show()
        
#         logger.info("Desktop AI Assistant with Voice started successfully")
        
        
#         sys.exit(app.exec_())
        
#     except NameError as e:
#         if "'true' is not defined" in str(e):
#             logger.error("ERROR: Found 'true' instead of 'True' in code.")
#             logger.error("Please search your code for lowercase 'true' and replace with uppercase 'True'")
#             logger.error("Common places to check:")
#             logger.error("1. config.json - make sure it's valid JSON")
#             logger.error("2. Any Python files using 'true' instead of 'True'")
#             logger.error("3. Messaging settings or other boolean values")
#         logger.error(f"NameError: {str(e)}")
#         logger.error(traceback.format_exc())
#         sys.exit(1)
        
#     except Exception as e:
#         logger.error(f"Failed to start application: {str(e)}")
#         logger.error(traceback.format_exc())
#         sys.exit(1)

# if __name__ == "__main__":
#     main()



# STAND alone
import sys
import os
import logging
import traceback

# Handle standalone execution
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = os.path.dirname(sys.executable)
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(application_path, 'src'))

def main():
    try:
        from src.gui.main_window import MainWindow
        from src.nlp.model_handler import ModelHandler
        from src.executor.action_executor import ActionExecutor
        from src.utils.logger import setup_logging
        from src.utils.config import Config
        from PyQt5.QtWidgets import QApplication
        
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
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
        # Basic logging if advanced logging fails
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to start application: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Show error message to user
        from PyQt5.QtWidgets import QMessageBox
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Application Error", 
                        f"Failed to start application:\n{str(e)}\n\nCheck logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
