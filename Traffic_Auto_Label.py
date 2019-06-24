import logging
import os
import subprocess
import json
import time
from calendar import timegm

cwd = os.path.dirname(__file__)

#Read and extract data from JSON file
def readJSONData():
    commandlist = list()
    timeutclist = list()
    epochlist = list()
    json_filename = os.path.join(cwd, '2019_06_11Traffic_Curation_files/IV_snoopyData.JSON')
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
        for p in data:
            #logging.info("first: "+ str(p))
            #logging.info("first: "+ str(p['snoopy_id']))
            #logging.info("second: "+ str(p['content']))
            #logging.info("third: "+ str(p['className']))
            #logging.info("fourth: "+ str(p['start']))
            if str(p['content']).find('nmap') != -1:
                commandlist.append(str(p['content']))
                timeutclist.append(str(p['start']))
                epochlist.append(timegm(time.strptime(str(p['start']), "%Y-%m-%dT%H:%M:%S")))
    logging.info(commandlist)
    logging.info(timeutclist)
    logging.info(epochlist)
    return float(epochlist[0]), commandlist

#Use tshark to get the framenumbers from the pcapng file
#Note: this is the command that requires init.lua to be disabled;known to happen if run as superuser
def tshark(epochtime):
    packets = list()
    packet_time = list()
    packet_frame = list()
    input_file = os.path.join(cwd, '2019_06_11Traffic_Curation_files/III_pivoting_capture_annotated_v2.pcapng')
    output = subprocess.check_output(["tshark", "-r", input_file, "-Y", '(frame.time_epoch >= 1508953300) && (frame.time_epoch <= 1560375581)', "-T", "fields", "-e", "frame.time_epoch", "-e", "frame.number"])
    output_file = os.path.join(cwd, 'timewframenum')
    file = open(output_file, 'w+')
    output = output.decode("utf-8")
    file.write(output)
    file = open(output_file, 'r')
    for line in file:
        packets.append(line)
        #logging.info(packets)
        if float(line[:20]) >= epochtime:
        #if float(epochtime) >= float(line[:20]):
            packet_time.append(float(line[:20]))
            packet_frame.append(int(line[21:-1]))
    file.close()
    #logging.info(packets)
    #logging.info(packet_time)
    #logging.info(packet_frame)
    os.remove(output_file)
    return packet_time, packet_frame

#Use editcap to add a comment to the frame numbers (within .1 second before and 1 second after) based on the data within the snoopy log.
def editcap(commandlist, first_command, packet_time, packet_frame):
    start = first_command - .1
    end = first_command + 1
    filtered_packet_time = list()
    filtered_packet_frame = list()
    for i in range(len(packet_time)):
        if packet_time[i] >= start and packet_time[i] <= end: #if the time falls inside 1.1 sec time frame add it
            filtered_packet_time.append(packet_time[i])
            filtered_packet_frame.append(packet_frame[i])
    logging.info(filtered_packet_time)
    logging.info(filtered_packet_frame)
    input_file = os.path.join(cwd, '2019_06_11Traffic_Curation_files/III_pivoting_capture_annotated_v2.pcapng')
    output_file = os.path.join(cwd, 'test_comment.pcapng')
    #insert for loop here to do all the frames
    framenumber = "1"
    testcomment = "start\ncmd: "+commandlist[0]
    subprocess.call(["editcap", input_file, output_file, "-a", framenumber+":"+testcomment])

if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.DEBUG)
    epochtime, commandlist = readJSONData()
    packet_time, packet_frame = tshark(epochtime)
    editcap(commandlist, epochtime, packet_time, packet_frame)
