import logging
import sys
import os, traceback
import shutil
import pprint
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, QSpinBox

from ECELDClient import ECELDClient

from GUI.Dialogs.JSONFolderDialog import JSONFolderDialog
from GUI.Dialogs.WiresharkFileDialog import WiresharkFileDialog
from GUI.Dialogs.ProgressBarWindow import ProgressBarWindow
from LogsToLuaDissector import getJSONFiles, readJSONData, eventsToDissector
from CommandLoad import CommandLoad
from WiresharkWindow import WiresharkWindow
from ValidatorRunner import ValidatorRunner
import time

from PyQt5.QtWidgets import QMessageBox

class MainApp(QMainWindow):
    RAW_DATA_EXPORT_PATH = "/tmp/logdatapivot/"
    OUTDATA_PATH = "/tmp/logdatapivot/outpivot/"
    OUTDATA_PCAP_FILENAME = "NeedsComments.pcapng"

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

        self.log_stop_button = QPushButton('Logger Stop and Process')
        self.log_stop_button.clicked.connect(self.on_log_stop_button_clicked)
        self.log_stop_button.setEnabled(False)

        wireshark_annotate_label = QLabel('Step I. Use Wireshark to Add Comments to Log')
        wireshark_annotate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        wireshark_annotate_label.setAlignment(Qt.AlignCenter)

        self.wireshark_annotate_button = QPushButton('Run Wireshark')
        self.wireshark_annotate_button.clicked.connect(self.on_wireshark_annotate_button_clicked)
        self.wireshark_annotate_button.setEnabled(True)

        validate_label = QLabel('Step II. Find Incidents in Another Network File Based on Comments')
        validate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        validate_label.setAlignment(Qt.AlignCenter)

        self.wireshark_file_button = QPushButton('Select File')
        self.wireshark_file_button.clicked.connect(self.on_wireshark_file_button_clicked)
        self.wireshark_file_button.setEnabled(False)

        self.wireshark_file_lineedit = QLineEdit()
        self.wireshark_file_lineedit.setText('Please select a pcap or pcapng file')
        self.wireshark_file_lineedit.setAlignment(Qt.AlignLeft)
        self.wireshark_file_lineedit.setReadOnly(True)
        self.wireshark_file_lineedit.setEnabled(False)

        self.validate_button = QPushButton('Find Incidents')
        self.validate_button.clicked.connect(self.on_validate_button_clicked)
        self.validate_button.setEnabled(False)

        # log_start_layout.addWidget(self.log_start_button)
        # log_stop_layout.addWidget(self.log_stop_button)
        wireshark_annotate_layout.addWidget(self.wireshark_annotate_button)

        validate_layout.addWidget(self.wireshark_file_button)
        validate_layout.addWidget(self.wireshark_file_lineedit)
        
        # mainlayout.addWidget(log_start_label)
        # mainlayout.addLayout(log_start_layout)
        # mainlayout.addStretch()
        # mainlayout.addWidget(log_stop_label)
        # mainlayout.addLayout(log_stop_layout)
        # mainlayout.addStretch()
        mainlayout.addWidget(wireshark_annotate_label)
        mainlayout.addLayout(wireshark_annotate_layout)
        mainlayout.addStretch()
        mainlayout.addWidget(validate_label)
        mainlayout.addLayout(validate_layout)
        mainlayout.addWidget(self.validate_button)
        mainlayout.addStretch()
        mainwidget.setLayout(mainlayout)
        self.dissectors_generated = []
        self.eclient = ECELDClient.ECELDClient()
        logging.info("MainWindow(): Complete")
    
    def on_log_start_button_clicked(self):
        logging.info('on_log_start_button_clicked(): Instantiated')
        self.eclient.startCollectors()
        self.log_start_button.setEnabled(False)
        self.log_stop_button.setEnabled(True)
        self.wireshark_annotate_button.setEnabled(False)
        self.wireshark_file_button.setEnabled(False)
        self.wireshark_file_lineedit.setEnabled(False)
        self.validate_button.setEnabled(False)
        logging.info('on_log_start_button_clicked(): Complete')

    def on_log_stop_button_clicked(self):
        logging.info('on_log_stop_button_clicked(): Instantiated')
        self.eclient.stopCollectors()
        self.eclient.parseDataAll()
        self.eclient.exportData("/tmp/logdata")
        #get the most recent exported directory:
        latestlogsdir = ""
        mydir = os.path.join(MainApp.RAW_DATA_EXPORT_PATH)
        latestlogdirs = self.getSortedInDirs(mydir, dircontains="export")
        latestlogdir = ""
        if len(latestlogdirs) > 0:
            #get the latest
            latestlogdir = latestlogdirs[-1]
        else:
            logging.error("No export log file directory found in path: " + MainApp.RAW_DATA_EXPORT_PATH)
            return
        try:
            if os.path.exists(MainApp.OUTDATA_PATH) == False:
                os.makedirs(MainApp.OUTDATA_PATH)
        except:
            logging.error("on_log_stop_button_clicked(): An error occured when trying create directory")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        try:
            #cp all JSON files to out dir
            snoopyFile = os.path.join(latestlogdir,"parsed","snoopy","snoopyData.JSON")
            keystrokesFile = os.path.join(latestlogdir,"parsed","pykeylogger","keypressData.JSON")
            if os.path.exists(snoopyFile):
                shutil.copy(snoopyFile,os.path.join(MainApp.OUTDATA_PATH,"SystemCalls.JSON"))
            if os.path.exists(keystrokesFile):
                shutil.copy(keystrokesFile,os.path.join(MainApp.OUTDATA_PATH,"Keypresses.JSON"))
            #cp merged pcap to dir
            pcapFile = os.path.join(latestlogdir,"raw","tshark","merged.pcapng")
            if os.path.exists(pcapFile):
                shutil.copy(pcapFile,os.path.join(MainApp.OUTDATA_PATH,MainApp.OUTDATA_PCAP_FILENAME))
        except:
            logging.error("on_log_stop_button_clicked(): An error occured when trying to copy log files")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        #create lua dissectors based on log data and store results into outdir
        self.command_thread = CommandLoad(log_directory=MainApp.OUTDATA_PATH)
        self.command_thread.signal.connect(self.update_progress_bar)
        self.command_thread.signal2.connect(self.thread_finish)
        self.progress_window = ProgressBarWindow(self.command_thread.getLoadCount())
        self.progress_window.show()
        self.command_thread.start()

        logging.info('on_log_stop_button_clicked(): Complete')

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
            self.log_stop_button.setEnabled(False)
            self.wireshark_annotate_button.setEnabled(True)
            self.wireshark_file_button.setEnabled(False)
            self.wireshark_file_lineedit.setEnabled(False)
            self.validate_button.setEnabled(False)

    def on_wireshark_annotate_button_clicked(self):
        logging.info('on_activate_wireshark_button_clicked(): Instantiated')
        #open wireshark using the captured pcap and the generated lua files
        self.dissectors_generated = ['/tmp/logdatapivot/output-dissectors/keypresses.lua', '/tmp/logdatapivot/output-dissectors/systemcalls.lua']
        self.wireshark_thread = WiresharkWindow(lua_scripts=self.dissectors_generated, pcap_filename=os.path.join(MainApp.OUTDATA_PATH,MainApp.OUTDATA_PCAP_FILENAME))
        self.wireshark_thread.start()
        self.log_start_button.setEnabled(True)
        self.log_stop_button.setEnabled(False)
        self.wireshark_annotate_button.setEnabled(True)
        self.wireshark_file_button.setEnabled(True)
        self.wireshark_file_lineedit.setEnabled(True)
        self.validate_button.setEnabled(False)
        logging.info('on_activate_wireshark_button_clicked(): Complete')

    def on_wireshark_file_button_clicked(self):
        logging.info('on_wireshark_file_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen == "":
            logging.error("File choose canceled")
            return
        self.wireshark_file_lineedit.setText(file_chosen)
        if self.wireshark_file_lineedit.text() != "Please select a pcap or pcapng file":
            self.log_start_button.setEnabled(True)
            self.log_stop_button.setEnabled(False)
            self.wireshark_annotate_button.setEnabled(True)
            self.wireshark_file_button.setEnabled(True)
            self.wireshark_file_lineedit.setEnabled(True)
            self.validate_button.setEnabled(True)
        logging.info('on_wireshark_file_button_clicked(): Complete')
    
    def on_validate_button_clicked(self):
        logging.info('on_validate_button_clicked(): Instantiated')
        self.validator_thread = ValidatorRunner(os.path.join(MainApp.OUTDATA_PATH,MainApp.OUTDATA_PCAP_FILENAME), self.wireshark_file_lineedit.text())
        self.validator_thread.start()
        self.log_start_button.setEnabled(True)
        self.log_stop_button.setEnabled(False)
        self.wireshark_annotate_button.setEnabled(True)
        self.wireshark_file_button.setEnabled(True)
        self.wireshark_file_lineedit.setEnabled(True)
        self.validate_button.setEnabled(True)
        logging.info('on_validate_button_clicked(): Complete')

    def getSortedInDirs(self, path, dircontains=""):
        logging.info('getSortedInDirs(): Instantiated')
        name_list = os.listdir(path)
        dirs = []
        for name in name_list:
            fullpath = os.path.join(path,name)
            if os.path.isdir(fullpath) and (dircontains in name):
                dirs.append(fullpath)
        logging.info('getSortedInDirs(): Completed')
        if dirs != None:
            return sorted(dirs)
        else:
            return []

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