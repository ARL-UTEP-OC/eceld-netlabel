import logging
import sys
import os
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, QSpinBox

#from ECELDClient import ECELDClient

from GUI.Dialogs.JSONFolderDialog import JSONFolderDialog
from GUI.Dialogs.WiresharkFileDialog import WiresharkFileDialog
from GUI.Dialogs.ProgressBarWindow import ProgressBarWindow
from LogsToLuaDissector import getJSONFiles, readJSONData, eventsToDissector
from CommandLoad import CommandLoad
from WiresharkWindow import WiresharkWindow

from PyQt5.QtWidgets import QMessageBox

class MainApp(QMainWindow):
    def __init__(self):
        logging.info("MainApp(): Instantiated")
        super(MainApp, self).__init__()
        self.setWindowTitle('Traffic Annotation Workflow')
        mainwidget = QWidget()
        self.setCentralWidget(mainwidget)
        mainlayout = QVBoxLayout()
        log_start_layout = QHBoxLayout()
        log_stop_layout = QHBoxLayout()
        wireshark_annotate_layout = QHBoxLayout()
        validate_layout = QHBoxLayout()

        log_start_label = QLabel('Step I. Start Logging Network Data and Actions')
        log_start_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        log_start_label.setAlignment(Qt.AlignCenter)

        self.log_start_button = QPushButton('Logger Start')
        self.log_start_button.clicked.connect(self.on_log_start_button_clicked)

        log_stop_label = QLabel('Step II. Stop Logging Network Data and Actions')
        log_stop_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        log_stop_label.setAlignment(Qt.AlignCenter)

        self.log_stop_button = QPushButton('Logger Stop')
        self.log_stop_button.clicked.connect(self.on_log_stop_button_clicked)

        wireshark_annotate_label = QLabel('Step III. Use Wireshark to Add Comments to Logs')
        wireshark_annotate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        wireshark_annotate_label.setAlignment(Qt.AlignCenter)

        self.wireshark_annotate_button = QPushButton('Run Wireshark')
        self.wireshark_annotate_button.clicked.connect(self.on_wireshark_annotate_button_clicked)
        self.wireshark_annotate_button.setEnabled(False)

        validate_label = QLabel('Step IV. Find Incidents in Another Network File Based on Comments')
        validate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        validate_label.setAlignment(Qt.AlignCenter)

        self.wireshark_file_button = QPushButton('Select File')
        self.wireshark_file_button.clicked.connect(self.on_wireshark_file_button_clicked)
        self.wireshark_file_button.setEnabled(False)

        self.wireshark_file_lineedit = QLineEdit()
        self.wireshark_file_lineedit.setText('Please select a pcap or pcapng file')
        self.wireshark_file_lineedit.setAlignment(Qt.AlignLeft)
        self.wireshark_file_lineedit.setReadOnly(True)

        self.validate_button = QPushButton('Find Incidents')
        self.validate_button.clicked.connect(self.on_validate_button_clicked)
        self.validate_button.setEnabled(False)

        log_start_layout.addWidget(self.log_start_button)
        log_stop_layout.addWidget(self.log_stop_button)
        wireshark_annotate_layout.addWidget(self.wireshark_annotate_button)

        validate_layout.addWidget(self.wireshark_file_button)
        validate_layout.addWidget(self.wireshark_file_lineedit)
        
        mainlayout.addWidget(log_start_label)
        mainlayout.addLayout(log_start_layout)
        mainlayout.addStretch()
        mainlayout.addWidget(log_stop_label)
        mainlayout.addLayout(log_stop_layout)
        mainlayout.addStretch()
        mainlayout.addWidget(wireshark_annotate_label)
        mainlayout.addLayout(wireshark_annotate_layout)
        mainlayout.addStretch()
        mainlayout.addWidget(validate_label)
        mainlayout.addLayout(validate_layout)
        mainlayout.addWidget(self.validate_button)
        mainlayout.addStretch()
        mainwidget.setLayout(mainlayout)
        self.dissectors_generated = []
        #self.eclient = ECELDClient.ECELDClient()
        logging.info("MainWindow(): Complete")
    
    def on_log_start_button_clicked(self):
        logging.info('on_log_start_button_clicked(): Instantiated')
        self.eclient.startCollectors()
        self.log_start_button.setEnabled(False)
        self.log_stop_button.setEnabled(True)
        self.wireshark_annotate_button.setEnabled(False)
        self.validate_button.setEnabled(False)
        logging.info('on_log_start_button_clicked(): Complete')

    def on_log_stop_button_clicked(self):
        logging.info('on_log_stop_button_clicked(): Instantiated')
        self.eclient.stopCollectors()
        self.log_start_button.setEnabled(True)
        self.log_stop_button.setEnabled(False)
        self.wireshark_annotate_button.setEnabled(True)
        self.validate_button.setEnabled(False)
        logging.info('on_log_stop_button_clicked(): Complete')

    def on_annotate_button_clicked(self):
        logging.info('on_annotate_button_clicked(): Instantiated')
        self.command_thread = CommandLoad(self.json_file.text(), self.wireshark_file.text(), self.left_spinbox.value(), self.right_spinbox.value())
        self.command_thread.signal.connect(self.update_progress_bar)
        self.command_thread.signal2.connect(self.thread_finish)
        self.progress_window = ProgressBarWindow(self.command_thread.getLoadCount())
        self.progress_window.show()

        self.command_thread.start()
        logging.info('on_annotate_button_clicked(): Complete')

    def update_progress_bar(self):
        self.progress_window.update_progress()
        self.progress_window.show()

    def thread_finish(self):
        logging.info('CommandLoad(): Thread Finished')
        self.progress_window.hide()
        self.dissectors_generated = self.command_thread.getCompleted()
        output_dissected = "Files generated:\r\n"
        for dissected in self.dissectors_generated:
            output_dissected += dissected + "\r\n"
        if output_dissected == "":
            QMessageBox.alert(self, "Processing Complete", "No files processed")
        else: 
            QMessageBox.about(self, "Processing Complete", output_dissected)
            self.log_start_button.setEnabled(True)
            self.log_stop_button.setEnabled(True)
            self.wireshark_annotate_button.setEnabled(True)
            self.validate_button.setEnabled(True)

    def on_wireshark_annotate_button_clicked(self):
        logging.info('on_activate_wireshark_button_clicked(): Instantiated')

        #parse, export, and then cp stuff where it's needed
        self.eclient.exportData(path="/tmp/logdata/")
        #self.wireshark_thread = WiresharkWindow(lua_scripts=self.dissectors_generated, pcap_filename=self.wireshark_file.text())
        #self.wireshark_thread.start()
        self.log_start_button.setEnabled(True)
        self.log_stop_button.setEnabled(False)
        self.wireshark_annotate_button.setEnabled(True)
        self.validate_button.setEnabled(True)
        logging.info('on_activate_wireshark_button_clicked(): Complete')

    def on_wireshark_file_button_clicked(self):
        logging.info('on_wireshark_file_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen != "":
            self.wireshark_file_lineedit.setText(file_chosen)
        if self.wireshark_file_lineedit.text() != "Please select a folder" and self.wireshark_file.text() != "Please select a pcap or pcapng file":
            self.log_start_button.setEnabled(True)
            self.log_stop_button.setEnabled(True)
            self.wireshark_annotate_button.setEnabled(True)
            self.validate_button.setEnabled(True)
        logging.info('on_wireshark_file_button_clicked(): Complete')
    
    def on_validate_button_clicked(self):
        pass


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