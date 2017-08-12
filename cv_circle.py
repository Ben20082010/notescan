import cv2
import numpy as np



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

cv2.imwrite("x.jpg",blur)

# opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

ret,thresh = cv2.threshold(blur,127,255,0)
viewPage(im)
# viewPage(mask)
# viewPage(blur)
# viewPage(im_gray)

circles = cv2.HoughCircles(im_gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0,)
circles = np.uint16(np.around(circles))
print('x')
for i in circles[0,:]:
    cv2.circle(im, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.circle(im, (i[0], i[1]), 2, (0, 0, 255), 3)
viewPage(im)