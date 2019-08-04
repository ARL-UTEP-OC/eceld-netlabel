import logging
import os
from PyQt5.QtCore import QThread, pyqtSignal
from LogsToLuaDissector import getJSONFiles, readJSONData, eventsToDissector

class CommandLoad(QThread):
    signal = pyqtSignal()
    signal2 = pyqtSignal()

    def __init__(self, log_directory, beforePacketTime = 0, afterPacketTime = 2):
        logging.info('CommandLoad(): Instantiated')
        QThread.__init__(self)
        self.beforePacketTime = beforePacketTime
        self.afterPacketTime = afterPacketTime
        #get files in directory
        self.filelist = getJSONFiles(log_directory)
        self.completed_dissector_filenames = []
        logging.info('CommandLoad(): Completed')

    def getLoadCount(self):
        return len(self.filelist)
    
    def getCompleted(self):
        return self.completed_dissector_filenames

    def run(self):
        logging.info('CommandLoad.run(): Instantiated')
        
        file_events = {}
        self.completed_dissector_filenames = []

        if os.path.exists("output-dissectors") == False:
            os.makedirs("output-dissectors")

        for filename in self.filelist:
            #save the filename as a key, all the events (event, time) as the value
            file_events = readJSONData(filename)
            base = os.path.basename(filename)
            basenoext = os.path.splitext(base)[0]
            dissector_filename = eventsToDissector(file_events, dissector_name=basenoext, ofilename="output-dissectors/"+basenoext, template_filename="templates/timebased.jnj2", start_threshold=0, end_threshold=2)
            self.completed_dissector_filenames.append(dissector_filename)
            #emit when file done reading
            self.signal.emit()
        logging.debug("main(): Dissector Files Created: " + str(self.completed_dissector_filenames))
        logging.info("main(): Complete")
        self.signal2.emit()
        logging.info('CommandLoad.run(): Completed')
