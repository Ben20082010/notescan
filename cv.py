import cv2
import numpy as np


def getHsvThreshold(RGB):
    hsv = cv2.cvtColor(np.uint8([[RGB]]), cv2.COLOR_RGB2HSV)[0][0]
    print(hsv)

    # low=[hsv[0]-10,90,155 ]
    # high=[hsv[0]+10,160,224]

    low=[hsv[0]-20,40,100 ]
    high=[hsv[0]+20,160,255]
    return np.array(low), np.array(high)


def viewPage(image):
    view=cv2.resize(image, (0,0), fx=0.35, fy=0.35)
    cv2.imshow('view', view)
    cv2.waitKey()

# im = cv2.imread('page-0.jpg')
im = cv2.imread('sample-0.jpg')
im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

lower_blue, upper_blue = getHsvThreshold([91, 155, 213])
mask = cv2.inRange(im_hsv, lower_blue, upper_blue)
blur=cv2.medianBlur(mask,3)


ret,thresh = cv2.threshold(blur,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

if hierarchy.max() != 5 :
    # #counter debug
    cv2.drawContours(im, contours, -1, (0,255,0), 50)
    cv2.imwrite('mask.jpg', mask)
    viewPage(mask)
    viewPage(blur)
    print('Does not have 7 contours (%s)' % hierarchy.max())
    idx = 0
    for cnt in contours:
        idx += 1

        im3 = cv2.imread('sample-0.jpg')
        x, y, w, h = cv2.boundingRect(cnt)
        roi = im3[y:y + h, x:x + w]
        cv2.imwrite('%s.jpg' % idx, roi)

        cv2.drawContours(im3, [cnt], -1, (0, 255, 0), 50)
        viewPage(im3)
    raise Exception('Does not have 7 contours (%s)' % hierarchy.max())
# print(hierarchy)




