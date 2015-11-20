import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
start = time.time()
current = time.time()
while(current - start < 60):
    ret, frame = cap.read()
    if ret==True:

        # write the flipped frame
        out.write(frame)

        #cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
	
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()