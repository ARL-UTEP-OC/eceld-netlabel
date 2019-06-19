import logging
import os
import subprocess
import json
import time
from calendar import timegm


def readJSONData():
    commandlist = list()
    timeutclist = list()
    epochlist = list()
    with open('/root/Desktop/Traffic/snoopyData.JSON', 'r') as json_file:
        data = json.load(json_file)
        for p in data:
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
    return float(epochlist[0])

#use tshark to get the framenumbers from the pcapng file
def tshark(epochtime):
    packets = list()
    packet_time = list()
    packet_frame = list()
    output = subprocess.check_output(["tshark", "-r", "/root/Desktop/Traffic/test.pcapng", "-Y", '(frame.time_epoch >= 1551220737.521798140) && (frame.time_epoch <= 1560375581)', "-T", "fields", "-e", "frame.time_epoch", "-e", "frame.number"])
    file = open('/root/Desktop/Traffic/timewframenum', 'w+')
    output = output.decode("utf-8")
    file.write(output)
    file = open('/root/Desktop/Traffic/timewframenum', 'r')
    for line in file:
        packets.append(line)
        if float(line[:20]) >= epochtime:
        #if float(epochtime) >= float(line[:20]):
            packet_time.append(float(line[:20]))
            packet_frame.append(int(line[21:-1]))
    file.close()
    logging.info(packets)
    logging.info(packet_time)
    logging.info(packet_frame)
    os.remove('/root/Desktop/Traffic/timewframenum')
    return packet_time, packet_frame

#Use editcap to add a comment to the frame numbers (within .1 second before and 1 second after) based on the data within the snoopy log.
def editcap(first_command, packet_time, packet_frame):
    start = first_command - .1
    end = first_command + 1
    filtered_packet_time = list()
    filtered_packet_frame = list()
    for i in range(len(packet_time)):
        if packet_time[i] >= start and packet_time[i] <= end: #if the time falls inside time frame add it
            filtered_packet_time.append(packet_time[i])
            filtered_packet_frame.append(packet_frame[i])
    logging.info(filtered_packet_time)
    logging.info(filtered_packet_frame)
    framenumber = "1"
    testcomment = "I was here"
    subprocess.call(["editcap", "/root/Desktop/Traffic/test.pcapng", "/root/Desktop/Traffic/test_comment.pcapng", "-a", framenumber+":"+testcomment])

if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.DEBUG)
    epochtime = readJSONData()
    packet_time, packet_frame = tshark(epochtime)
    editcap(epochtime, packet_time, packet_frame)
