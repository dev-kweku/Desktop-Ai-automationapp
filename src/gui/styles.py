def get_stylesheet():
    return """
    QMainWindow {
        background-color: #f0f0f0;
    }
    
    QLabel {
        padding: 5px;
    }
    
    QTextEdit {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        font-family: 'Courier New', monospace;
    }
    
    QLineEdit {
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 12px;
    }
    
    QPushButton {
        background-color: #4a86e8;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #3a76d8;
    }
    
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
    
    QPushButton#exit_button {
        background-color: #e87474;
    }
    
    QPushButton#exit_button:hover {
        background-color: #d86464;
    }
    """