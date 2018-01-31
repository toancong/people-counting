import cv2 as cv
import darknet as dn
from random import randint
import numpy as np

def rndBGR():
    return (randint(0,255), randint(0,255), randint(0,255))

def toTlBr(bbox):
    bbox = np.int0(bbox)
    tl = (bbox[0], bbox[1])
    br = (bbox[0] + bbox[2], bbox[1] + bbox[3])
    return tl, br

if __name__ == "__main__":
    # this is example
    net = dn.load_net(b"/darknet/cfg/yolo.cfg", b"/darknet/yolo.weights", 0)
    meta = dn.load_meta(b"/darknet/cfg/coco.data")

    r = dn.detect(net, meta, b"/darknet/data/dog.jpg")
    print(r)

    img = cv.imread("/darknet/data/dog.jpg")
    for i in r:
        c = rndBGR()
        tl, br = toTlBr(i[2])
        cv.rectangle(img, tl, br, c, 2)
        cv.putText(img, i[0].decode("utf-8"), (tl[0], tl[1] + 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2,cv.LINE_AA)
    cv.imshow('detect', img)
    # r = dn.detect(net, meta, b'/darknet/data/horses.jpg')
    # print(r)
    # r = dn.detect(net, meta, b'/darknet/data/person.jpg')
    # print(r)
    cv.waitKey(0)
    cv.destroyAllWindows()
