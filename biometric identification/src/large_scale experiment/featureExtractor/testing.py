import numpy as np;
from ML import FeatureExtractor

data = np.array([[-7.360646,74.324404],[-10.182022,74.707892],[217.06201,73.735476],[-3.525766,73.749172],[217.06201,72.858932],[217.06201,71.585204],
 [-10.127238,74.40658],[217.06201,73.215028],[-1.622022,73.3109],[217.06201,74.13266],[217.06201,74.20114],[-3.525766,74.653108],[217.06201,74.762676],
[-2.128774,73.79026],[173.98809,73.434164],[174.234618,72.119348],[174.563322,67.873588],[174.686586,67.887284],[175.371386,65.887668],[175.028986,72.270004],
[175.261818,72.475444],[176.206842,63.970228],[176.631418,61.998004],[177.179258,59.327284],[177.234042,75.529652],[217.06201,69.558196],
 [176.823162,50.137268],[176.631418,49.75378],[176.302714,101.195956],[175.891834,49.82226],[175.63161,100.812468],[175.042682,100.113972],[174.440058,47.302196],[174.248314,46.590004],
 [173.933306,46.083252],[173.71417,45.959988],[173.207418,45.069748],[173.070458,43.823412],[172.741754,36.372788],[172.098042,63.942836],[170.933882,-143.031116],
 [169.74233,74.420276],[169.002746,74.310708],[168.92057,74.584628]])
avg = FeatureExtractor.getAvgHeight(data)
print 'avg height:' + str(avg)
circ = FeatureExtractor.getcircumference(data, 50.0)
print "circumference: ",circ