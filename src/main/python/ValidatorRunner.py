import logging
import subprocess
import shlex
import sys
import os
from PyQt5.QtCore import QThread

class ValidatorRunner(QThread):
    VALIDATOR_PATH = "/root/git/eceld-traffic-validator/scripts/"
    VALIDATOR_FILENAME = "validate_train.sh"
    VALIDATOR_SOLN_PATH = "/root/git/eceld-traffic-validator/sample-ranking-files/"
    VALIDATOR_SOLN_FILENAME = "pivot_soln.JSON"

    def __init__(self, commented_pcap_filename, validate_pcap_filename):
        logging.info('ValidatorRunner(): Instantiated')
        QThread.__init__(self)
        self.cmd = os.path.join(ValidatorRunner.VALIDATOR_PATH, ValidatorRunner.VALIDATOR_FILENAME)
        self.cmd = self.cmd + " " + commented_pcap_filename + " " + validate_pcap_filename
        self.cmd = self.cmd + " " + os.path.join(ValidatorRunner.VALIDATOR_SOLN_PATH, ValidatorRunner.VALIDATOR_SOLN_FILENAME)
        logging.info('ValidatorRunner(): Complete')

    def run(self):
        logging.info('ValidatorRunner.run(): Instantiated')
        if sys.platform == "linux" or sys.platform == "linux2":
            output = subprocess.check_output(shlex.split(self.cmd), encoding="utf-8")
        else: 
            output = subprocess.check_output(self.cmd, encoding="utf-8")

        logging.info('ValidatorRunner.run(): Complete')

