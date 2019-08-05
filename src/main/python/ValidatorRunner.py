import logging
import subprocess
import shlex
import sys
from PyQt5.QtCore import QThread

class ValidatorRunner(QThread):
    VALIDATOR_PATH = "/root/git/eceld-traffic-validator/"
    VALIDATOR_FILENAME = "validate_train.sh"

    def __init__(self, pcap_filename=None):
        logging.info('ValidatorRunner(): Instantiated')
        QThread.__init__(self)
        self.cmd = ValidatorRunner.WIRESHARK_PATH + ValidatorRunner.VALIDATOR_FILENAME
        if pcap_filename != None:
            self.cmd+= " " + pcap_filename
        else:
            logging.error("ValidatorRunner(): No pcapng specified! Not processing.")
            return
        logging.info('ValidatorRunner(): Complete')

    def run(self):
        logging.info('ValidatorRunner.run(): Instantiated')
        if sys.platform == "linux" or sys.platform == "linux2":
            output = subprocess.check_output(shlex.split(self.cmd), encoding="utf-8")
        else: 
            output = subprocess.check_output(self.cmd, encoding="utf-8")

        logging.info('ValidatorRunner.run(): Complete')

