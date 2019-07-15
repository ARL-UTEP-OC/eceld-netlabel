import logging
import sys
import os
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar

from GUI.Dialogs.JSONFileDialog import JSONFileDialog
from GUI.Dialogs.WiresharkFileDialog import WiresharkFileDialog
from GUI.Dialogs.ProgressBarWindow import ProgressBarWindow
from Traffic_Auto_Label import readJSONData, getFrameNums, injectComment
from CommandLoad import CommandLoad
from WiresharkWindow import WiresharkWindow

class MainApp(QMainWindow):
    def __init__(self):
        logging.info("MainApp(): Instantiated")
        super(MainApp, self).__init__()
        self.setWindowTitle('ECEL Automatic Net Label')
        mainwidget = QWidget()
        self.setCentralWidget(mainwidget)
        mainlayout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        label1 = QLabel('Pick a JSON data file:')
        label1.setAlignment(Qt.AlignCenter)

        json_button = QPushButton('JSON file')
        json_button.clicked.connect(self.on_json_button_clicked)

        self.json_file = QLineEdit()
        self.json_file.setText('Nothing has been selected')
        self.json_file.setAlignment(Qt.AlignCenter)
        self.json_file.setDisabled(True)

        label2 = QLabel('Pick a Wireshark file')
        label2.setAlignment(Qt.AlignCenter)

        wireshark_button = QPushButton('Wireshark file')
        wireshark_button.clicked.connect(self.on_wireshark_button_clicked)

        self.wireshark_file = QLineEdit()
        self.wireshark_file.setText('Nothing has been selected')
        self.wireshark_file.setAlignment(Qt.AlignCenter)
        self.wireshark_file.setDisabled(True)

        label3 = QLabel('Click the annotate button once\nyou are ready to comment the pcapng file')
        label3.setAlignment(Qt.AlignCenter)

        annotate_button = QPushButton('Annotate')
        annotate_button.clicked.connect(self.on_annotate_button_clicked)

        label4 = QLabel('To open up wireshark click the button below')
        label4.setAlignment(Qt.AlignCenter)

        activate_wireshark_button = QPushButton('Run Wireshark')
        activate_wireshark_button.clicked.connect(self.on_activate_wireshark_button_clicked)

        layout1.addWidget(json_button)
        layout1.addWidget(self.json_file)

        layout2.addWidget(wireshark_button)
        layout2.addWidget(self.wireshark_file)
        
        mainlayout.addWidget(label1)
        mainlayout.addLayout(layout1)
        mainlayout.addStretch()
        mainlayout.addWidget(label2)
        mainlayout.addLayout(layout2)
        mainlayout.addStretch()
        mainlayout.addWidget(label3)
        mainlayout.addWidget(annotate_button)
        mainlayout.addStretch()
        mainlayout.addWidget(label4)
        mainlayout.addWidget(activate_wireshark_button)
        mainlayout.addStretch()
        mainwidget.setLayout(mainlayout)
        logging.info("MainWindow(): Complete")
    
    def on_json_button_clicked(self):
        logging.info('on_json_button_clicked(): Instantiated')
        file_chosen = JSONFileDialog().json_dialog()
        self.json_file.setText(file_chosen)
        logging.info('on_json_button_clicked(): Complete')

    def on_wireshark_button_clicked(self):
        logging.info('on_wireshark_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        self.wireshark_file.setText(file_chosen)
        logging.info('on_wireshark_button_clicked(): Complete')

    def on_annotate_button_clicked(self):
        logging.info('on_annotate_button_clicked(): Instantiated')
        eventlist = readJSONData(self.json_file.text())
        self.window = ProgressBarWindow(int(len(eventlist)))
        self.window.show()
        self.command_thread = CommandLoad()
        self.command_thread.eventlist = eventlist
        self.command_thread.wireshark_file = self.wireshark_file.text()
        self.command_thread.signal.connect(self.update_progress_bar)
        self.command_thread.signal2.connect(self.thread_finish)
        self.command_thread.start()
        logging.info('on_annotate_button_clicked(): Complete')

    def update_progress_bar(self):
        self.window.update_progress()
        self.window.show()

    def thread_finish(self):
        logging.info('CommandLoad(): Thread Finished')
        self.window.hide()

    def on_activate_wireshark_button_clicked(self):
        logging.info('on_activate_wireshark_button_clicked(): Instantiated')
        self.wireshark_thread = WiresharkWindow()
        self.wireshark_thread.start()
        logging.info('on_activate_wireshark_button_clicked(): Complete')

if __name__ == '__main__':
    logging.info("main(): Instantiated")
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.DEBUG)
    appctxt = ApplicationContext()
    app = MainApp()
    app.setGeometry(500, 300, 500, 150)
    app.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
    logging.info("main(): Complete")