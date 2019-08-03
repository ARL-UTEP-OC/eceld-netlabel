import time
import logging
import os
import sys, traceback
from subprocess import Popen
import Pyro4

class ECELDClient():
    def __init__(self):
        logging.info("Instantiating ecel_manager()")
        #start the nameserver
        logging.debug("ecel_manager(): attempting to start the pyro name server")

        logging.debug("ecel_manager(): getting a handle to the ecel.service")
        self.ecel_manager = Pyro4.Proxy("PYRONAME:ecel.service")    # use name server object lookup uri shortcut
    
    def startCollectors(self):
        logging.debug("startCollectors(): requesting to remove all data")
        self.ecel_manager.remove_data()
        logging.debug("startCollectors(): requesting to start collectors")
        self.ecel_manager.start_collectors()

    def stopCollectors(self):
        logging.debug("stopCollectors(): requesting to stop collectors")
        self.ecel_manager.stop_collectors()

    def exportData(self, path=None):
        logging.debug("exportData(): requesting to export data to " + str(path))
        try:
            if os.path.exists() == False:
                logging.debug("exportData(): requesting to export data to " + str(path))
                os.path.mkdirs(path)
        except:
            logging.error("exportData(): An error occured when trying to use path for export: " + str(path))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        ecel_manager.export_data(path)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Instantiating ECELDClient()")

    logging.info("Completed ECELDClient()")