import logging
import os
import subprocess


def readJSONData():
    #file1 = open('G:/ARL/Traffic Detection/JSON_Data/snoopyData.JSON', 'r')
    file1 = open('E:/ARL/Traffic Detection/JSON_Data/snoopyData.JSON', 'r')
    #file2 = open('G:/ARL/Traffic Detection/JSON_Data/filteredTimeStamps', 'w+')
    file2 = open('E:/ARL/Traffic Detection/JSON_Data/filteredTimeStamps', 'w+')
    for line in file1:
        if line[3:12] == 'snoopy_id':
            start_timestamp = line[-23:-3]
            file2.write(start_timestamp+'\n')
            logging.info(start_timestamp)
    file1.close()
    file2.close()
    timearraysort()

def timearraysort():
    timestamparray = []
    #file = open('G:/ARL/Traffic Detection/JSON_Data/filteredTimeStamps', 'r')
    file = open('E:/ARL/Traffic Detection/JSON_Data/filteredTimeStamps', 'r')
    for line in file:
        if line[0] != '"':
            timestamparray.append(line[:19])
        if line[0] == '"':
            timestamparray.append(line[1:-1])
    print(timestamparray)

#use tshark to get the framenumbers from the pcapng file
def tshark():
    #subprocess.Popen(, stdout=subprocess.PIPE) #This is where i write the location of tshark executable (do i need stdout=subprocess.PIPE)
    #subprocess.call(['tshark', '-r test.pcapng', '-Y "(frame.time_epoch >= 1551220737.521798140) && (frame.time_epoch <= 1551220737.535983541)"', '-T fields', '-e frame.time_epoch', '-e frame.number
    #', '> G:/ARL/Traffic Detection/JSON_Data/filteredFrameNumbers'])
    #subprocess.call(['tshark', '-r test.pcapng', '-Y "(frame.time_epoch >= 1551220737.521798140) && (frame.time_epoch <= 1551220737.535983541)"', '-T fields', '-e frame.time_epoch', '-e frame.number
    #', '> E:/ARL/Traffic Detection/JSON_Data/filteredFrameNumbers'])
    #subprocess.terminate()
    """
    file = open('E:/ARL/Traffic Detection/JSON_Data/filteredFrameNumbers', 'r')
    for line in file:
        
    """
    hello = []

#Use editcap to add a comment to the frame numbers (within .1 second before and 1 second after) based on the data within the snoopy log.
def editcap():
    hello = []

if __name__=="__main__":
    print('hello')
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.DEBUG)
    logging.debug('woot')
    logging.info('WHaaat!')
    logging.warning('woah thats bad')
    readJSONData()
    tshark()
    #editcap()
    os.remove('G:/ARL/Traffic Detection/JSON_Data/filteredTimeStamps') #Need  to move this to end of readJSONData