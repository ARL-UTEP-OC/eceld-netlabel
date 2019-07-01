import sys
import logging
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout, QMessageBox, QFileDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from Traffic_Auto_Label import readJSONData, getFrameNums, injectComment


class MainWindow(QWidget):
    def __init__(self):
        logging.info("MainWindow(): Instantiated")
        super(MainWindow, self).__init__()
        self.setWindowTitle('ECEL Automatic Net Label')
        mainlayout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        label1 = QLabel('Pick a JSON data file:')
        label1.setAlignment(Qt.AlignCenter)

        button1 = QPushButton('JSON file')
        button1.clicked.connect(self.on_button1_clicked)

        self.file_selected1 = QLineEdit()
        self.file_selected1.setText('Nothing has been selected')
        self.file_selected1.setAlignment(Qt.AlignCenter)
        self.file_selected1.setDisabled(True)

        label2 = QLabel('Pick a Wireshark file')
        label2.setAlignment(Qt.AlignCenter)

        button2 = QPushButton('Wireshark file')
        button2.clicked.connect(self.on_button2_clicked)

        self.file_selected2 = QLineEdit()
        self.file_selected2.setText('Nothing has been selected')
        self.file_selected2.setAlignment(Qt.AlignCenter)
        self.file_selected2.setDisabled(True)

        button_ok = QPushButton('OK')
        button_ok.clicked.connect(self.on_ok_clicked)

        layout1.addWidget(button1)
        layout1.addWidget(self.file_selected1)

        layout2.addWidget(button2)
        layout2.addWidget(self.file_selected2)

        mainlayout.addWidget(label1)
        mainlayout.addLayout(layout1)
        mainlayout.addStretch()
        mainlayout.addWidget(label2)
        mainlayout.addLayout(layout2)
        mainlayout.addStretch()
        mainlayout.addWidget(button_ok)
        self.setLayout(mainlayout)
        logging.info("MainWindow(): Complete")

    def on_button1_clicked(self):
        logging.info('on_button1_clicked(): Instantiated')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileName()", "", "JSON Files (*.JSON)", options=options)
        if  filename:
            logging.debug('on_button1_clicked(): File Selected: '+filename[0])
            self.file_selected1.setText(filename[0])
        logging.info('on_button2_clicked(): Complete')

    def on_button2_clicked(self):
        logging.info('on_button2_clicked(): Instantiated')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileName()", "", "Wireshark Files (*.pcapng)", options=options)
        if  filename:
            logging.debug('on_button2_clicked(): File Selected: '+filename[0])
            self.file_selected2.setText(filename[0])
        logging.info('on_button2_clicked(): Complete')

    def on_ok_clicked(self):
        logging.info('on_ok_clicked(): Instantiated')
        eventlist = readJSONData(self.file_selected1.text())
        for (event, time) in eventlist:
            startEpochTime = float(time) - 0.1
            endEpochTime = float(time) + 1
            logging.debug("on_ok_clicked(): Using start/stop: " + str(startEpochTime) + " " + str(endEpochTime))
            frameNums = getFrameNums(startEpochTime, endEpochTime, self.file_selected2.text())
            #Seems to get stuck on frameNums
            if frameNums != None:
                logging.debug("on_ok_clicked(): calling inject comment for Event: " + str(event) + " FrameNums: " + str(frameNums))
                injectComment(event, frameNums, self.file_selected2.text())
        logging.info('on_ok_clicked(): Complete')


if __name__=="__main__":
    logging.info("main(): Instantiated")
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.INFO)
    app = QApplication([])
    application = MainWindow()
    application.setGeometry(500, 300, 500, 150)
    application.show()
    app.exec_()
    logging.info("main(): Complete")