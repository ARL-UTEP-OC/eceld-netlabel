from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar

class ProgressBarWindow(QMainWindow):
    
    def __init__(self, bar_length):
        super().__init__()
        self.completed = 0
        self.setWindowTitle('Processing Data')
        self.setFixedSize(300, 100)
        self.progress_bar(bar_length)

    def progress_bar(self, bar_length):
        mainwidget = QWidget()
        self.setCentralWidget(mainwidget)
        mainlayout = QVBoxLayout()

        self.label4 = QLabel('Progress')
        self.label4.setAlignment(Qt.AlignCenter)
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(50, 40, 200, 20)
        self.progress.setMaximum(bar_length)
        
        mainlayout.addWidget(self.label4)
        mainlayout.addStretch()
        mainwidget.setLayout(mainlayout)

    def update_progress(self):
        self.completed += 1
        self.progress.setValue(self.completed)