# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:37:03 2019

@author: ezhu2
"""

import serial 
import time

minn = 1023 
maxx =  0

#  y1 = ((float(analogRead(A0)-minn)) / (maxx-minn))  * 1000;

serialPort = serial.Serial('COM7',115200, timeout = 0)
#serialPort2 = serial.Serial('COM9',115200, timeout = 0)

#Part of line location algorithm, don't worry about this
def correct_val(to_cor):
    global minn
    global maxx
    if (to_cor < minn):
        minn = to_cor -1
    if(to_cor > maxx):
        maxx = to_cor +1
    corrected = (to_cor - minn)/ (maxx-minn) * 1000
    return corrected

def turn_left(difference):
    return
def turn_right(difference):
    return

while 1:
    data = serialPort.readline() # Raw data from the sensor, is separated as 5 values from 0 to 1023 corresponding to each sensor
    datastr = data.decode()
    split_data = datastr.split("  ")
    corrected=[]
    if len(split_data) == 5:
        split_data[4] = split_data[4][0:len(split_data[4])- 2]# Simply to get rid of newline characters
        for i in range(5):
            corrected.append( correct_val(int(split_data[i])))
        # The following is the line localization algorithm. 
        line_loc = (0 * corrected[0] + 1000 * corrected[1] + 2000 * corrected[2] + 3000 * corrected[3] + 4000 * corrected[4])/(sum(corrected))
        print(serialPort.readline())
        print(split_data)
        print(corrected)
        print(line_loc)
        time.sleep(.25)
        
        #There are a few cases to keep track of
        #If only sensor 1 detects the black line, line_loc is approximately 2500,
        #Sensor 2 2200~, Sensor 3 2000~ (Goal), Sensor 4, 1800~, Sensor 5 1500
        #So if it is greater than 2000 turn left, less than 2000 turn right.
        #If sensor detects high value like 3000 or 1000, sharp turn is needed
        if(line_loc - 2000) > 0:
            turn_left(line_loc - 2000)
        elif(line_loc - 2000) < 0:
            turn_right(line_loc-2000) 
        