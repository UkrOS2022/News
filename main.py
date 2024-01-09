from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import subprocess
import requests
import os

class UpdateCenter(QWidget):
    def __init__(self):
        super().__init__()

        buttons = """
            QPushButton {
                background-color: #B1B1B1;
                color: black;
                border: 2px solid #B1B1B1;
                border-radius: 5px;
                padding: 8px;
            }
        
            QPushButton:hover {
                background-color: #8B8B8B;
                color: white;
            }
        """
        
        h1 = """
            QLabel {
                font-size: 30px;
            }
        """

        # Set up main window properties
        self.setWindowTitle(self.tr("Update Center"))
        self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(600, 400)
        icon = QIcon('icon.png')
        self.setWindowIcon(icon)
        self.setStyleSheet(buttons)
        
        
        # MAIN
        
        self.fast_checking_button = QPushButton("Fast to checking of updates", self)
        self.fast_checking_button.setGeometry(5, 5, 190, 35)
        self.fast_checking_button.clicked.connect(self.fast_checking)
        
        self.full_checking_button = QPushButton("Full to checking of updates", self)
        self.full_checking_button.setGeometry(5, 45, 190, 35)
        self.full_checking_button.clicked.connect(self.full_checking)
        
        self.home_button = QPushButton("Home", self)
        self.home_button.setGeometry(5, 320, 190, 35)
        self.home_button.clicked.connect(self.home)
        
        self.about_button = QPushButton("About", self)
        self.about_button.setGeometry(5, 360, 190, 35)
        self.about_button.clicked.connect(self.about)
        
        self.main_label = QLabel("Home", self)
        self.main_label.setGeometry(200, 5, 200, 30)
        self.main_label.setStyleSheet(h1)
        
        
        # "HOME" PAGE
        
        # Elements
        
        
        # "ABOUT" PAGE

        about = """
            Update Center
            Version: 1.0.0 beta
            Author: Vadym Savenko (UkrOS Company)
            """

        self.about_text = QLabel(about, self)
        self.about_text.setGeometry(200, 40, 390, 300)
        self.about_text.hide()
        

    def fast_checking(self):
        command = f'sudo apt update && sudo apt upgrade -y && sudo apt-get update && sudo apt-get upgrade -y'
        subprocess.run(['gnome-terminal', '--', 'bash', '-c', command])

    def updating_file(self):
        command = f'sudo rm command.txt && sudo wget https://ukros2022.github.io/UpdateCenter/command.txt'
        subprocess.run(['gnome-terminal', '--', 'bash', '-c', command])


    def full_checking(self):
        self.updating_file()
        with open('command.txt', 'r') as file:
            subprocess.run(['gnome-terminal', '--', 'bash', '-c', str(file.read())])



    def home(self):
        # HIDE
        self.about_text.hide()
        
        # SHOW
        # Elements
        
        # Changing of main label to "Home"
        self.main_label.setText("Home")
        
    def about(self):        
        # SHOW
        self.about_text.show()
        
        # Changing of main label to "About"
        self.main_label.setText("About")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = UpdateCenter()
    welcome_window.show()
    sys.exit(app.exec_())
