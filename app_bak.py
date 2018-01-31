import numpy as np
import cv2 as cv

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]
tracker = cv.MultiTracker_create()

cap = cv.VideoCapture('storage/sample.mp4')

fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

# setup initial location of window
track_window = (1,1,1,1)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 2, 1 )

fframe = None

while(1):
    ret, frame = cap.read()

    # return if end or ESC pressed
    if ret == False:
        break
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

    fgmask = fgbg.apply(frame)

    if fframe is None:
        fframe = fgmask
        height, width, channels = frame.shape
        centerHeight = int(height / 2) # center of height
        centerWidth = int(width / 2) # center of width
        # set up the ROI for tracking
        hsv_roi =  cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv.calcHist([hsv_roi],[0],fgmask,[180],[0,180])
        cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)
        continue

    # set up the ROI for tracking
    roi_hist = cv.calcHist([fgmask],[0], fgmask,[500],[0,500])
    dst = cv.calcBackProject([fgmask],[0],roi_hist,[0,500],1)

    # apply meanshift to get the new location
    ret, track_window = cv.CamShift(dst, track_window, term_crit)

    # Draw it on image
    pts = cv.boxPoints(ret)
    pts = np.int0(pts)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    res = cv.bitwise_and(frame,frame, mask= fgmask)
    res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    cv.imshow('res',res)

    cv.polylines(frame,[pts],True, 255, 2)
    cv.polylines(fgmask,[pts],True, 255, 2)

    cv.imshow('result',frame)
    cv.imshow('mask', fgmask)

cap.release()
cv.destroyAllWindows()