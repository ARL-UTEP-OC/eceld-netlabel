import time
import logging
import os
import sys, traceback
from subprocess import Popen, PIPE
import Pyro4
import shlex

class ECELDClient():
    ECELD_CALL_PATH = "/root/git/eceld/scripts/service_calls/"
    def __init__(self):
        logging.info("Instantiating ecel_manager()")
    
    def startCollectors(self):
        logging.debug("startCollectors(): requesting to remove all data")
        cmd = "/usr/bin/python " + ECELDClient.ECELD_CALL_PATH + "eceld_remove.py"
        logging.debug("startCollectors() running command: " + cmd)
        try:
            process = Popen(shlex.split(cmd), stdout=PIPE)
            logging.debug("startCollectors() waiting for system call to complete...")
            out, err = process.communicate()
            logging.debug("startCollectors() Completed.")

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("startCollectors(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return

        cmd = "/usr/bin/python " + ECELDClient.ECELD_CALL_PATH + "eceld_start.py"
        logging.debug("startCollectors() running command: " + cmd)
        try:
            process = Popen(shlex.split(cmd), stdout=PIPE)
            logging.debug("startCollectors() waiting for system call to complete...")
            out, err = process.communicate()
            logging.debug("startCollectors() Completed.")

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("startCollectors(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return

        logging.debug("startCollectors(): Complete")

    def stopCollectors(self):
        logging.debug("stopCollectors(): requesting to stop collectors")
        cmd = "/usr/bin/python " + ECELDClient.ECELD_CALL_PATH + "eceld_stop.py"
        logging.debug("startCollectors() running command: " + cmd)
        try:
            process = Popen(shlex.split(cmd), stdout=PIPE)
            logging.debug("startCollectors() waiting for system call to complete...")
            out, err = process.communicate()
            logging.debug("startCollectors() Completed.")

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("startCollectors(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return

        logging.debug("stopCollectors(): Complete")


    def exportData(self, path=None):
        logging.debug("exportData(): requesting to export data to " + str(path))
        if path == None:
            path = "/tmp/"

        try:
            if os.path.exists(path) == False:
                logging.debug("exportData(): requesting to export data to " + str(path))
                os.path.mkdirs(path)
        except:
            logging.error("exportData(): An error occured when trying to use path for export: " + str(path))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        cmd = "/usr/bin/python " + ECELDClient.ECELD_CALL_PATH + "eceld_export.py " + path
        logging.debug("startCollectors() running command: " + cmd)
        try:
            process = Popen(shlex.split(cmd), stdout=PIPE)
            logging.debug("startCollectors() waiting for system call to complete...")
            out, err = process.communicate()
            logging.debug("startCollectors() Completed.")

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("startCollectors(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return

        logging.debug("exportData(): Complete")

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Instantiating ECELDClient()")
    eclient = ECELDClient()
    logging.info("Starting Collectors")
    eclient.startCollectors()
    time.sleep(5)
    logging.info("Stopping Collectors")
    eclient.stopCollectors()
    logging.info("Completed ECELDClient()")
