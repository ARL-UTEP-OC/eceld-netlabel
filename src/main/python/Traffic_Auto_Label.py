import logging
import os
import sys, traceback
import subprocess
import json
import time
from calendar import timegm
import shlex

cwd = os.getcwd()

def getJSONFiles(folder_loc=None):
    logging.debug("getJSONFiles(): instantiated")
    #will hold the filenames
    filelist = list()
    try:
        if folder_loc:
            json_folder = folder_loc
        else:
            json_folder = os.path.join(cwd, './')
        logging.info("getJSONFiles(): reading filenames")
        for r, d, f in os.walk(json_folder):
            for file in f:
                if '.JSON' in file:
                    filelist.append(os.path.join(r, file))
        logging.debug("Found files: " + str(filelist))
        logging.info("getJSONFiles(): File reading complete")
        return (filelist)

    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.error("readJSONData(): An error occured ")
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        exit()	   

#Read and extract data from JSON file
def readJSONData(file_loc=None):
    logging.debug("readJSONData(): instantiated")
    #will hold the event and its timestamp
    eventlist = list()
    try:
        if file_loc:
            json_filename = file_loc
        else:
            json_filename = os.path.join(cwd, '2019_06_11Traffic_Curation_files/IV_snoopyData.JSON')
        logging.info("readJSONData(): reading file as json data")
        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)
            for p in data:
                logging.debug("readJSONData(): appending: " + (str(p['content']) + str(timegm(time.strptime(str(p['start']), "%Y-%m-%dT%H:%M:%S")) ) ))
                eventlist.append( (str(p['content']),timegm(time.strptime(str(p['start']), "%Y-%m-%dT%H:%M:%S"))) )
        logging.info("readJSONData(): File reading complete")
        return (eventlist)

    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.error("readJSONData(): An error occured ")
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        exit()		
        
#Use editcap to add a comment to the frame numbers (within .1 second before and 1 second after) based on the data within the snoopy log.
def injectComment(event, frameNums, file_loc=None):
    logging.debug("injectComment(): instantiated")
    if file_loc:
        input_file = file_loc
    else:
        input_file = os.path.join(cwd, '2019_06_11Traffic_Curation_files/III_pivoting_capture_annotated_v2.pcapng')
    output_file = os.path.join(cwd, 'auto_annotation.pcapng')
    #insert for loop here to do all the frames 
    logging.info("injectComment(): Adding comment to frames")
    for frameNum in frameNums:
        comment = "start\ncmd: " + event
        cmd = "editcap " + input_file + " " + output_file + " -a " + frameNum + ":\"" + comment + "\""
        logging.debug("injectComment(): running command: " + cmd)
        if sys.platform == "linux" or sys.platform == "linux2":
            output = subprocess.check_output(shlex.split(cmd), encoding="utf-8")
        else: 
            output = subprocess.check_output(cmd, encoding="utf-8")
        logging.debug("injectComment(): process output: " + str(output))
        logging.debug("injectComment(): Injecting comment Event: " + comment + "FrameNum: " + frameNum)

    logging.info("injectComment(): Completed adding comments to frames")

if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.DEBUG)
    logging.info("main(): Instantiated")
    filelist = getJSONFiles("/root/git/eceld-traffic-validator/sample-logs/")
    for filename in filelist:
        eventlist = readJSONData(filename)
        for (event, time) in eventlist:
            startEpochTime = float(time) - 0.1
            endEpochTime = float(time) + 1
            logging.debug("main(): Using start/stop: " + str(startEpochTime) + " " + str(endEpochTime))
            frameNums = getFrameNums(startEpochTime, endEpochTime, filename)
            if frameNums != None:
                logging.debug("main(): calling inject comment for Event: " + str(event) + " FrameNums: " + str(frameNums))
                injectComment(event, frameNums)
    logging.info("main(): Complete")