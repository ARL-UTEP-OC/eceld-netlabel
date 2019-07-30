import logging
import sys
import os
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, QSpinBox

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
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()

        json_label = QLabel('Pick a JSON data file:')
        json_label.setAlignment(Qt.AlignCenter)

        json_button = QPushButton('JSON file')
        json_button.clicked.connect(self.on_json_button_clicked)

        self.json_file = QLineEdit()
        self.json_file.setText('Nothing has been selected')
        self.json_file.setAlignment(Qt.AlignCenter)
        self.json_file.setDisabled(True)

        additional_json_label = QLabel('If you would like to add additional JSON files(Optional):')
        additional_json_label.setAlignment(Qt.AlignCenter)

        additional_json_button = QPushButton('Add JSON file')
        additional_json_button.clicked.connect(self.on_additional_json_button_clicked)

        self.additional_json_file = QLineEdit()
        self.additional_json_file.setText('Nothing has been selected')
        self.additional_json_file.setAlignment(Qt.AlignCenter)
        self.additional_json_file.setDisabled(True)

        wireshark_label = QLabel('Pick a Wireshark file')
        wireshark_label.setAlignment(Qt.AlignCenter)

        wireshark_button = QPushButton('Wireshark file')
        wireshark_button.clicked.connect(self.on_wireshark_button_clicked)

        self.wireshark_file = QLineEdit()
        self.wireshark_file.setText('Nothing has been selected')
        self.wireshark_file.setAlignment(Qt.AlignCenter)
        self.wireshark_file.setDisabled(True)

        left_time_label = QLabel('Select the time range before the\n first initial packet is found(sec)')
        left_time_label.setAlignment(Qt.AlignCenter)

        right_time_label = QLabel('Select the time range after the\n first initial packet is found(sec)')
        right_time_label.setAlignment(Qt.AlignCenter)

        self.left_spinbox = QDoubleSpinBox()
        self.left_spinbox.setSingleStep(.1)
        self.left_spinbox.setMinimum(.1)

        self.right_spinbox = QSpinBox()
        self.right_spinbox.setMinimum(1)

        annotate_label = QLabel('Click the annotate button once\nyou are ready to comment the pcapng file')
        annotate_label.setAlignment(Qt.AlignCenter)

        annotate_button = QPushButton('Annotate')
        annotate_button.clicked.connect(self.on_annotate_button_clicked)

        wireshark2_label = QLabel('To open up wireshark click the button below')
        wireshark2_label.setAlignment(Qt.AlignCenter)

        activate_wireshark_button = QPushButton('Run Wireshark')
        activate_wireshark_button.clicked.connect(self.on_activate_wireshark_button_clicked)

        layout1.addWidget(json_button)
        layout1.addWidget(self.json_file)

        layout2.addWidget(additional_json_button)
        layout2.addWidget(self.additional_json_file)

        layout3.addWidget(wireshark_button)
        layout3.addWidget(self.wireshark_file)

        layout4.addWidget(left_time_label)
        layout4.addWidget(right_time_label)

        layout5.addWidget(self.left_spinbox)
        layout5.addWidget(self.right_spinbox)
        
        mainlayout.addWidget(json_label)
        mainlayout.addLayout(layout1)
        mainlayout.addStretch()
        mainlayout.addWidget(additional_json_label)
        mainlayout.addLayout(layout2)
        mainlayout.addStretch()
        mainlayout.addWidget(wireshark_label)
        mainlayout.addLayout(layout3)
        mainlayout.addStretch()
        mainlayout.addLayout(layout4)
        mainlayout.addLayout(layout5)
        mainlayout.addStretch()
        mainlayout.addWidget(annotate_label)
        mainlayout.addWidget(annotate_button)
        mainlayout.addStretch()
        mainlayout.addWidget(wireshark2_label)
        mainlayout.addWidget(activate_wireshark_button)
        mainlayout.addStretch()
        mainwidget.setLayout(mainlayout)
        logging.info("MainWindow(): Complete")
    
    def on_json_button_clicked(self):
        logging.info('on_json_button_clicked(): Instantiated')
        file_chosen = JSONFileDialog().json_dialog()
        self.json_file.setText(file_chosen)
        logging.info('on_json_button_clicked(): Complete')

    def on_additional_json_button_clicked(self):
        logging.info('on_additional_json_button_clicked(): Instantiated')
        file_chosen = JSONFileDialog().json_dialog()
        self.additional_json_file.setText(file_chosen)
        logging.info('on_additional_json_button_clicked(): Complete')

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
        self.command_thread.beforePacketTime = self.left_spinbox.value()
        self.command_thread.afterPacketTime = self.right_spinbox.value()
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