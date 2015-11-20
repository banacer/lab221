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

def write_event_data(event_file, event_data, len, current_time):
    for i in range(0,len):
        event_file.write(str(event_data[i,0])+','+str(event_data[i,1])+'\n')
    event_file.write(str(current_time) + '_\n')
    event_file.flush()

ser = Serial('/dev/ttyACM0',9600)

count= 0
temperature = 23
calibration_a = 0.013696
calibration_b = -3.56201
event = []
eventCount = 0
all_data_file = open('all_data.dat','a')
raw_event_file = open('event_raw.data', 'a')
feature_file = open('features.dat','a')
log_file = open('readline.log','a')

while True:
    try:
        line = ser.readline()
        current_time = time.time()
        count +=1
        data = line.split(',')

        all_data_file.write(str(current_time)+','+line+'\n')
        all_data_file.flush()
        if len(data) == 3:
            for i in range(0,3):
                val =re.sub('[^0-9]','', data[i])
                #data[i] = int(val)#((float(val) / 10**4 ) * (331.3 + 0.606 * temperature)) / 2
                data[i] = calibration_a * float(val) + calibration_b;

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
                feature_line =  str(avgHeight)+','+ str(maxHeight)+','+ str(avgWidth)+ ','+ str(maxWidth) + ',' + str(circumference)
                #print feature_line
                feature_file.write(str(current_time)+','+feature_line+'\n')
                feature_file.flush()
                write_event_data(raw_event_file,eventdata,eventCount,current_time)

                #initialize vars for next event
                eventCount = 0
                event = []
    except Exception:
        t = time.time()
        print 'error'
        log_file.write('An error occured at ' + str(t))
        pass