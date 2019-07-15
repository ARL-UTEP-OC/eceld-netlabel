import logging
from PyQt5.QtCore import QThread, pyqtSignal
from Traffic_Auto_Label import getFrameNums, injectComment

class CommandLoad(QThread):
    signal = pyqtSignal()
    signal2 = pyqtSignal()

    def __init__(self):
        logging.info('CommandLoad(): Instantiated')
        QThread.__init__(self)
        self.eventlist = None
        self.wireshark_file = ""
        logging.info('CommandLoad(): Completed')

    def run(self):
        logging.info('CommandLoad.run(): Instantiated')
        for (event, time) in self.eventlist:
            print('event: '+event+' time: '+str(time))
            startEpochTime = float(time) - 0.1
            endEpochTime = float(time) + 1
            logging.debug("on_ok_clicked(): Using start/stop: " + str(startEpochTime) + " " + str(endEpochTime))
            frameNums = getFrameNums(startEpochTime, endEpochTime, self.wireshark_file)
            #Seems to get stuck on frameNums
            if frameNums != None:
                logging.debug("on_ok_clicked(): Calling inject comment for Event: " + str(event) + " FrameNums: " + str(frameNums))
                injectComment(event, frameNums, self.wireshark_file)
            self.signal.emit()
        self.signal2.emit()
        logging.info('CommandLoad.run(): Completed')
