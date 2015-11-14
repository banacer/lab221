import re
from serial import Serial
import time
import numpy as np
import ML.FeatureExtractor as features

def get_height_and_width(data):
    measures = []
    measures.append(213.5 - float(data[0]))
    measures.append(112 - float(data[1]) - float(data[2]))
    return measures        

ser = Serial('/dev/ttyACM0',9600)
start = time.time()
count= 0
temperature = 23
calibration_a = 0.013696
calibration_b = -3.56201
event = []
eventCount = 0
raw = open('event_raw.data', 'a')
feature_file = open('features.dat','a')

while True:       
    line = ser.readline()    
    count +=1
    data = line.split(',')
    if len(data) == 3:    
        for i in range(0,3):
            val =re.sub('[^0-9]','', data[i])
            #data[i] = int(val)#((float(val) / 10**4 ) * (331.3 + 0.606 * temperature)) / 2
            data[i] = calibration_a * float(val) + calibration_b;            
        t = time.time()       
        measures = get_height_and_width(data)
        
        if (110 < measures[0] and measures[0] < 200) or measures[1] > 20:  #start of passing event
            #print "measures: ",measures
            event.append(measures)
            eventCount += 1
        elif eventCount > 5: # extract features            
            eventdata = np.array(event)
            avgHeight = features.getAvgHeight(eventdata)
            maxHeight = features.getMaxHeight(eventdata)
            avgWidth = features.getAvgWidth(eventdata)
            maxWidth = features.getMaxWidth(eventdata)
            circumference = features.getcircumference(eventdata, 50.0)
            print avgHeight,",", maxHeight,",", avgWidth, ",", maxWidth , "," ,circumference 
            
            
            #initialize vars for next event
            eventCount = 0
            event = []

