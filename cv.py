import cv2
import numpy as np


def getHsvThreshold(RGB):
    hsv = cv2.cvtColor(np.uint8([[RGB]]), cv2.COLOR_RGB2HSV)[0][0]
    print (hsv)
    low=[hsv[0]-10,50,50]
    high=[hsv[0]+10,255,255]

    return np.array(low), np.array(high)

im = cv2.imread('page-0.jpg')
im_org=im
im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

lower_blue, upper_blue = getHsvThreshold([91, 155, 213])
mask = cv2.inRange(im_hsv, lower_blue, upper_blue)

ret,thresh = cv2.threshold(mask,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    im3 = cv2.imread('page-0.jpg')
    cv2.drawContours(im3, [cnt], -1, (0, 255, 0), 3)
    im3 = cv2.resize(im3, (0,0), fx=0.4, fy=0.4)
    cv2.imshow('im', im3)
    cv2.waitKey()