import numpy as np
import cv2
import time
import readline

def capture(id):
    cap = cv2.VideoCapture(0)
    #set the camera_done boolean value to false
    readline.camera_done = False

    # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter('output'+str(id)+'.avi', fourcc, 25.0, (640, 480))
    start = time.time()
    current = time.time()
    while current - start < 10:
        print (current - start)
        ret, frame = cap.read()
        current = time.time()
        if ret == True:
            # write the flipped frame
            out.write(frame)

            # cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    #Setting camera footage as done
    readline.camera_done = True
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def extract_video_event(start, end, video,id):
    cap = cv2.VideoCapture('videos/output'+str(id)+'.avi')
    nFrames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter(video, fourcc, 25.0, (640, 480))
    f_start = start * 25
    f_end = end * 25
    print nFrames
    print fps
    print f_start
    print f_end

    for count in xrange( nFrames ):
        ret, frame = cap.read()
        #print 'count: ' + str(count)
        if f_start <= count and count <= f_end:
            out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


#capture()
extract_video_event(2, 5, 'video.avi')
