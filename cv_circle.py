import cv2
import numpy as np
import matplotlib.pyplot as plt
from func import *


def getHsvThreshold(RGB):
    hsv = cv2.cvtColor(np.uint8([[RGB]]), cv2.COLOR_RGB2HSV)[0][0]

    # low=[hsv[0]-10,90,155 ]
    # high=[hsv[0]+10,160,224]

    low=[hsv[0]-20,80,80 ]
    high=[hsv[0]+20,255,255]
    return np.array(low), np.array(high)


def viewPage(image):
    view=cv2.resize(image, (0,0), fx=1, fy=1)
    cv2.imshow('view', view)
    cv2.waitKey()
    cv2.destroyAllWindows()

def findCircle(cnts,tolerance=0.10):
    list=[] #[x,y,r]
    for cnt in cnts:
        # smallest circle
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        # get r from area
        area = cv2.contourArea(cnt)
        r2 = np.sqrt(4 * area / np.pi) / 2

        uncertanity=(radius-r2)/r2
        print('circle uncertainty is %s ' %uncertanity)
        if uncertanity < tolerance:
            list.append([x,y,r2])  # as radius may be affected by extreme value.
    return list




# path='cache/t15.jpg'
# path='cache/temp/3.5.jpg'
# path='cache/temp/3-4.jpg'
path='cache/pagexxx.png'

# path='cache/page-0.jpg'
# path='cache/t15.jpg'



im = cv2.imread(path)
# im = cv2.imread('cache/1.jpg')
im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


lower_blue, upper_blue = getHsvThreshold([91, 155, 213])
mask = cv2.inRange(im_hsv, lower_blue, upper_blue)
blur=cv2.medianBlur(mask,11 )


# opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

ret,thresh = cv2.threshold(blur,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

viewPage(im)
# viewPage(mask)
viewPage(blur)


xyrs=findCircle(contours)
xyrs=np.array(xyrs).astype(int)
for xyr in xyrs:
    x,y,r=xyr
    cv2.circle(im,(x,y),r,(0,0,255),5)

# # Perspective Transformation
xys=np.delete(xyrs, -1, axis=1)
xys=order_points(xys)
print(xys)
pts1 = np.float32(xys)
pts2 = np.float32([[0,0],[875,0],[875,1254],[0,1254]])

M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(im,M,(875,1254))

plt.subplot(121),plt.imshow(im),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()

