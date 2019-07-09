import logging
import os
import sys
import subprocess
import json
import time
from calendar import timegm
import shlex

cwd = os.path.dirname(__file__)

#Read and extract data from JSON file
def readJSONData(file_loc=None):
    logging.debug("readJSONData(): instantiated")
    #will hold the event and its timestamp
    eventlist = list()
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

#Use tshark to get the framenumbers from the pcapng file
#Note: this is the command that requires init.lua to be disabled;known to happen if run as superuser
def getFrameNums(startEpochTime, endEpochTime, file_loc=None):
    logging.debug("getFrameNums(): instantiated")
    frameNums = list()
    if file_loc:
        input_file = file_loc
    else:
        input_file = os.path.join(cwd, '2019_06_11Traffic_Curation_files/III_pivoting_capture_annotated_v2.pcapng')
    cmd = "tshark -r " + input_file + " -Y \"(frame.time_epoch >= "+str(startEpochTime) +") && (frame.time_epoch <= "+str(endEpochTime) +")\" -T fields -e frame.number"
    logging.debug("getFrameNums(): running command: " + cmd)
    logging.info("getFrameNums(): Matching frame numbers with timestamps between " + str(startEpochTime) +" to " + str(endEpochTime))
    if sys.platform == "linux" or sys.platform == "linux2":
        output = subprocess.check_output(shlex.split(cmd), encoding="utf-8")
    else:
        output = subprocess.check_output(cmd, encoding="utf-8")
    logging.debug("getFrameNums(): process output: " + str(output))
    for line in output.split("\n"):
        if line != "":
            frameNums.append(line.strip())
    logging.debug("getFrameNums(): Frame list: " + str(frameNums))
    if frameNums == []:
        logging.info("getFrameNums(): No frames matching timestamps found ")
        return None
    logging.info("getFrameNums(): Frame matching completed")
    return frameNums

#Use editcap to add a comment to the frame numbers (within .1 second before and 1 second after) based on the data within the snoopy log.
def injectComment(event, frameNums, file_loc=None, custom_comment=None):
    logging.debug("injectComment(): instantiated")
    if file_loc:
        input_file = file_loc
    else:
        input_file = os.path.join(cwd, '2019_06_11Traffic_Curation_files/III_pivoting_capture_annotated_v2.pcapng')
    output_file = os.path.join(cwd, 'auto_annotation.pcapng')
    #insert for loop here to do all the frames 
    logging.info("injectComment(): Adding comment to frames")
    for frameNum in frameNums:
        if custom_comment:
            comment = "start\ncmd: " + event + "\nExtra comment:\n" + custom_comment
        else:
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
    eventlist = readJSONData()
    for (event, time) in eventlist:
        startEpochTime = float(time) - 0.1
        endEpochTime = float(time) + 1
        logging.debug("main(): Using start/stop: " + str(startEpochTime) + " " + str(endEpochTime))
        frameNums = getFrameNums(startEpochTime, endEpochTime)
        if frameNums != None:
            logging.debug("main(): calling inject comment for Event: " + str(event) + " FrameNums: " + str(frameNums))
            injectComment(event, frameNums)
    logging.info("main(): Complete")