import numpy as np
from scipy.spatial import distance
speed = 5

def getAvgHeight(data):    
    return np.mean(data[0<data[:,0],0])

def getMaxHeight(data):
    return np.max(data[0<data[:,0],0])

def getAvgWidth(data):
    return np.mean(data[0<data[:,1],1])

def getMaxWidth(data):
    return np.max(data[0<data[:,1],1])

def getcircumference(data,sampling_rate):    
    beg = data[0,1]    
    side = 0
    size = data[:,1].size
    previous_point = np.array([0,0])
    my_distance = timeToDistance(sampling_rate)
    for i in range(1,size - 1):
        if data[i,1] < 0:
            continue
        current_point = np.array([data[i,1],i*my_distance])        
        euclidean_distance = distance.euclidean(current_point, previous_point)
        if euclidean_distance > 5:
            continue
        print "euclidean distance: ", euclidean_distance
        previous_point = current_point
        side += euclidean_distance/2
    end = data[size - 1,1]
    circumference = beg + end + 2 * side
    return circumference
    
def timeToDistance(sampling_rate):
    distancePerMillisecond = float(speed) *100000 / (3600*1000)
    distance = 1000/sampling_rate * distancePerMillisecond 
    return distance
  