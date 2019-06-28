import sys
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout, QMessageBox, QFileDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout


class MainWindow(QWidget):
    def __init__(self):
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
        self.setLayout(mainlayout)

    def on_button1_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileName()", "", "JSON Files (*.JSON)", options=options)
        if  filename:
            print(filename)
            self.file_selected1.setText(filename[0])

    def on_button2_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileName()", "", "Wireshark Files (*.pcapng)", options=options)
        if  filename:
            print(filename)
            self.file_selected2.setText(filename[0])


if __name__=="__main__":
    app = QApplication([])
    application = MainWindow()
    application.setGeometry(500, 300, 500, 150)
    application.show()
    app.exec_()