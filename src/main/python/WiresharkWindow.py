import logging
import subprocess
from PyQt5.QtCore import QThread

class WiresharkWindow(QThread):

    def __init__(self):
        logging.info('WiresharkWindow(): Instantiated')
        QThread.__init__(self)
        logging.info('WiresharkWindow(): Complete')

    def run(self):
        logging.info('WiresharkWindow.run(): Instantiated')
        subprocess.run(["wireshark"])
        logging.info('WiresharkWindow.run(): Complete')