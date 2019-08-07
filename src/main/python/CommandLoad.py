import logging
import os
from PyQt5.QtCore import QThread, pyqtSignal
from LogsToLuaDissector import getJSONFiles, readJSONData, eventsToDissector
import time

class CommandLoad(QThread):
    signal = pyqtSignal()
    signal2 = pyqtSignal()

    def __init__(self):
        logging.info('CommandLoad(): Instantiated')
        QThread.__init__(self)
        self.functionlist = []
        logging.info('CommandLoad(): Completed')

    def addFunction(self, funcname, *args):
        logging.info('CommandLoad.addFunction(): Instantiated')
        self.functionlist.append((funcname, *args))
        logging.info('CommandLoad.addFunction(): Complete')

    def getLoadCount(self):
        return len(self.functionlist)
    
    def run(self):
        logging.info('CommandLoad.run(): Instantiated')
        
        for ((funcname, *args)) in self.functionlist:
            #run the function with provided arguments
            funcname(*args)
            #emit when file done reading
            self.signal.emit()
        self.signal2.emit()
        logging.info('CommandLoad.run(): Completed')