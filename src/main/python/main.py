import logging
import sys
import os
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, QSpinBox


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
        self.setWindowTitle('ECEL Automatic Net Label')
        mainwidget = QWidget()
        self.setCentralWidget(mainwidget)
        mainlayout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()

        label1 = QLabel('Step I. Select the folder with the log files')
        label1.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        label1.setAlignment(Qt.AlignCenter)

        json_button = QPushButton('Log Directory')
        json_button.clicked.connect(self.on_json_button_clicked)

        self.json_file = QLineEdit()
        self.json_file.setText('Please select a folder with log files')
        self.json_file.setAlignment(Qt.AlignLeft)
        self.json_file.setReadOnly(True)

        label2 = QLabel('Step II. Select the Wireshark file')
        label2.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        label2.setAlignment(Qt.AlignCenter)

        self.wireshark_button = QPushButton('Wireshark file')
        self.wireshark_button.clicked.connect(self.on_wireshark_button_clicked)

        self.wireshark_file = QLineEdit()
        self.wireshark_file.setText('Please select a pcap or pcapng file')
        self.wireshark_file.setAlignment(Qt.AlignLeft)
        self.wireshark_file.setReadOnly(True)

        label3 = QLabel('Step III. Indicate time range before the\n first initial packet is found(sec)')
        label3.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        label3.setAlignment(Qt.AlignCenter)

        label4 = QLabel('Step IV. Indicate the time range after the\n first initial packet is found(sec)')
        label4.setAlignment(Qt.AlignCenter)
        label4.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))

        self.left_spinbox = QDoubleSpinBox()
        self.left_spinbox.setSingleStep(0.1)
        self.left_spinbox.setMinimum(0)
        self.left_spinbox.setValue(0)
        self.left_spinbox.setEnabled(False)

        self.right_spinbox = QDoubleSpinBox()
        self.right_spinbox.setSingleStep(0.1)
        self.right_spinbox.setMinimum(0.0)
        self.right_spinbox.setValue(2.0)
        self.right_spinbox.setEnabled(False)

        label5 = QLabel('Step V. Click the generate button to\ninject log data into the Wireshark file')
        label5.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        label5.setAlignment(Qt.AlignCenter)

        self.annotate_button = QPushButton('Inject Data')
        self.annotate_button.setEnabled(False)
        self.annotate_button.clicked.connect(self.on_annotate_button_clicked)

        label6 = QLabel('Step VI. Open the modified Wireshark file')
        label6.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        label6.setAlignment(Qt.AlignCenter)

        self.activate_wireshark_button = QPushButton('Open Wireshark File')
        self.activate_wireshark_button.setEnabled(False)
        self.activate_wireshark_button.clicked.connect(self.on_activate_wireshark_button_clicked)

        layout1.addWidget(json_button)
        layout1.addWidget(self.json_file)

        layout2.addWidget(self.wireshark_button)
        layout2.addWidget(self.wireshark_file)

        layout3.addWidget(label3)
        layout3.addWidget(label4)

        layout4.addWidget(self.left_spinbox)
        layout4.addWidget(self.right_spinbox)
        
        mainlayout.addWidget(label1)
        mainlayout.addLayout(layout1)
        mainlayout.addStretch()
        mainlayout.addWidget(label2)
        mainlayout.addLayout(layout2)
        mainlayout.addStretch()
        mainlayout.addLayout(layout3)
        mainlayout.addLayout(layout4)
        mainlayout.addStretch()
        mainlayout.addWidget(label5)
        mainlayout.addWidget(self.annotate_button)
        mainlayout.addStretch()
        mainlayout.addWidget(label6)
        mainlayout.addWidget(self.activate_wireshark_button)
        mainlayout.addStretch()
        mainwidget.setLayout(mainlayout)
        self.dissectors_generated = []
        logging.info("MainWindow(): Complete")
    
    def on_json_button_clicked(self):
        logging.info('on_json_button_clicked(): Instantiated')
        file_chosen = JSONFolderDialog().json_dialog()
        if file_chosen != "":
            self.json_file.setText(file_chosen)
        if self.json_file.text() != "Please select a folder" and self.wireshark_file.text() != "Please select a pcap or pcapng file":
            self.annotate_button.setEnabled(True)
            self.left_spinbox.setEnabled(True)
            self.right_spinbox.setEnabled(True)
            self.activate_wireshark_button.setEnabled(False)
        logging.info('on_json_button_clicked(): Complete')

    def on_wireshark_button_clicked(self):
        logging.info('on_wireshark_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen != "":
            self.wireshark_file.setText(file_chosen)
        if self.json_file.text() != "Please select a folder" and self.wireshark_file.text() != "Please select a pcap or pcapng file":
            self.annotate_button.setEnabled(True)
            self.left_spinbox.setEnabled(True)
            self.right_spinbox.setEnabled(True)
            self.activate_wireshark_button.setEnabled(False)
        logging.info('on_wireshark_button_clicked(): Complete')

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
            self.activate_wireshark_button.setEnabled(True)

    def on_activate_wireshark_button_clicked(self):
        logging.info('on_activate_wireshark_button_clicked(): Instantiated')
        self.wireshark_thread = WiresharkWindow(lua_scripts=self.dissectors_generated, pcap_filename=self.wireshark_file.text())
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