from random import randint
import time
import cv2 as cv
import math
import numpy as np

class MyPerson:
    tracks = []
    def __init__(self, i, xi, yi, max_age, tracker, contour):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
        self.tracker = tracker
        self.contour = contour

    def getContour(self):
        return self.contour
    def setContour(self, contour):
        self.contour = contour
    def getTracker(self):
        return self.tracker
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getState(self):
        return self.state
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done
    def going_UP(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end: #cruzo la linea
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start: #cruzo la linea
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False
    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
    def isMe(self, contour):
        x,y,w,h = cv.boundingRect(self.contour)
        x2,y2,w2,h2 = cv.boundingRect(contour)
        dist = math.sqrt((x + w/2 - x2 - w2/2)**2 + (y + h/2 - y2 - h2/2)**2)
        return dist <= w and dist <= h/2

def isPerson(contour):
    x,y,w,h = cv.boundingRect(contour)
    s = cv.contourArea(contour)
    if s < 700 or s > 15000:
        return False
    if w > h:
        return False
    return True
