import argparse
import datetime
import math
import cv2 as cv
import numpy as np
import Person
import darknet as dn
from random import randint

cap = cv.VideoCapture('app/storage/sample.mp4')
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

fframe = None
kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

font = cv.FONT_HERSHEY_SIMPLEX
persons = []
pid = 1
max_p_age = 5

term_crit = ( cv.TERM_CRITERIA_COUNT | cv.TERM_CRITERIA_EPS, 20, 0.03 )
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[1]
def createTracker():
    if tracker_type == 'BOOSTING':
        tracker = cv.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv.TrackerGOTURN_create()
    return tracker

def isInZoneLimit(bbox):
    x,y,w,h = bbox
    inZone = (width/6 < x + w/2 < width*5/6) and (0 < y + h/2 < height)
    return inZone

def isDetectIn(bbox, lineDetectIn):
    tl, br = toTlBr(bbox)
    tl2, br2 = toTlBr(lineDetectIn)
    return tl[0] <= br2[0] and br[0] >= tl2[0] and tl[1] <= br2[1] and br[1] >= tl2[1]

def toTlBr(bbox):
    bbox = np.int0(bbox)
    tl = (bbox[0], bbox[1])
    br = (bbox[0] + bbox[2], bbox[1] + bbox[3])
    return tl, br

def rndBGR():
    return (randint(0,255), randint(0,255), randint(0,255))

mt = cv.MultiTracker_create()
count = 0
zone = None
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
lineDetectIn = None

net = dn.load_net(b"/darknet/cfg/yolo.cfg", b"/darknet/yolo.weights", 0)
meta = dn.load_meta(b"/darknet/cfg/coco.data")
print('loaded darknet')

while 1:

    ret, frame = cap.read()

    # return if end or ESC pressed
    if ret == False:
        break
    k = cv.waitKey(10) & 0xff
    if k == 27:
        break

    if zone is None:
        # Init in first frame
        height, width, _ = frame.shape
        zone = (width/6, 0, width*4/6, height)
        zone = np.int0(zone)
        lineDetectIn = (width*5/6, 0, 0, height)
        lineDetectIn = np.int0(lineDetectIn)

    # dnimg = dn.array_to_image(frame)
    # dn.rgbgr_image(dnimg)
    # r = dn.detect2(net, meta, dnimg)
    # print(r)
    # cv.imshow('Result', frame)
    # continue

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (11, 11), 0)
    fgframe = fgbg.apply(gray)

    threshFrame = cv.threshold(fgframe, 10, 255, cv.THRESH_BINARY)[1]
    mask = cv.morphologyEx(threshFrame, cv.MORPH_OPEN, kernelOp)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernelCl)

    _, cnts, _ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for c in cnts:
        if not Person.isPerson(c):
            continue

        bbox = cv.boundingRect(c)
        if not isInZoneLimit(bbox):
            for i in persons:
                if i.isMe(c):
                    persons.remove(i)
            continue

        M = cv.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        new = True
        for i in persons:
            if i.isMe(c):
                cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.5,i.getRGB(),1,cv.LINE_AA)
                new = False
                cv.circle(frame,(cx, cy), 2, COLOR_RED, -1)
                i.updateCoords(cx,cy)
                i.setContour(c)

        if new == True:
            if not isDetectIn(bbox, lineDetectIn):
                continue
            tracker = createTracker()
            tracker.init(mask, bbox)
            mt.add(tracker, frame, bbox)

            p = Person.MyPerson(pid,cx,cy, max_p_age, tracker, c)
            persons.append(p)
            pid += 1
            count += 1

        tl, br = toTlBr(bbox)
        cv.rectangle(frame, tl, br, COLOR_GREEN, 2)
        cv.drawContours(frame, c, -1, COLOR_GREEN, 3, 8)

    # mt.update(frame)
    # for i in persons:
    #     trk = i.getTracker()
    #     ret, bbox = trk.update(frame)
    #     tl, br = toTlBr(bbox)
    #     cv.rectangle(frame, tl, br, COLOR_BLUE, 2)

    # for i in range(len(mt.getObjects())):
    #     bbox = mt.getObjects()[i]
    #     if isInZoneLimit(bbox):
    #         tl, br = toTlBr(bbox)
    #         cv.rectangle(frame, tl, br, COLOR_RED, 2)

    cv.putText(frame, 'Count: ' + str(count),(int(width/2),50),font,0.5, COLOR_RED,1,cv.LINE_AA)
    tl, br = toTlBr(zone)
    cv.rectangle(frame, tl, br, COLOR_BLUE, 2)
    tl, br = toTlBr(lineDetectIn)
    cv.line(frame, tl, br, COLOR_RED, 2)
    # cv.rectangle(fgframe, tl, br, COLOR_WHITE, 2)
    # cv.rectangle(mask, tl, br, COLOR_WHITE, 2)

    # cv.imshow('fgframe', fgframe)
    # cv.imshow('mask', mask)
    cv.imshow('Result', frame)

cap.release()
cv.destroyAllWindows()
