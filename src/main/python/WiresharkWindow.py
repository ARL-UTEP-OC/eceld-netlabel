import logging
import subprocess
import shlex
import sys
from PyQt5.QtCore import QThread

class WiresharkWindow(QThread):
    WIRESHARK_PATH="wireshark"

    def __init__(self, lua_scripts=None, pcap_filename=None):
        logging.info('WiresharkWindow(): Instantiated')
        QThread.__init__(self)
        self.cmd = WiresharkWindow.WIRESHARK_PATH
        if pcap_filename != None:
            self.cmd+= " -r " + pcap_filename
        if lua_scripts != None and len(lua_scripts) > 0:
            for lua_script in lua_scripts:
                self.cmd+= " -Xlua_script:" + lua_script
        logging.info('WiresharkWindow(): Complete')

    def run(self):
        logging.info('WiresharkWindow.run(): Instantiated')
        if sys.platform == "linux" or sys.platform == "linux2":
            output = subprocess.check_output(shlex.split(self.cmd), encoding="utf-8")
        else: 
            output = subprocess.check_output(self.cmd, encoding="utf-8")

        logging.info('WiresharkWindow.run(): Complete')

