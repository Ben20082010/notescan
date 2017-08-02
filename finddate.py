import cv2
import numpy as np
from PIL import Image
import pytesseract



def getHsvThreshold(RGB):
    hsv = cv2.cvtColor(np.uint8([[RGB]]), cv2.COLOR_RGB2HSV)[0][0]

    # low=[hsv[0]-10,90,155 ]
    # high=[hsv[0]+10,160,224]

    low=[hsv[0]-10,40,100 ]
    high=[hsv[0]+10,160,255]
    return np.array(low), np.array(high)


def viewPage(image,name='view'):
    view=cv2.resize(image, (0,0), fx=0.35, fy=0.35)
    cv2.imshow(name, view)
    cv2.waitKey()

def debugcnt(cnt,image,name='view'):
    x, y, w, h = cv2.boundingRect(cnt)
    roi = image[y:y + h, x:x + w]
    viewPage(roi,name)
    print(cv2.contourArea(cnt))

# im = cv2.imread('page-0.jpg')
im = cv2.imread('cache/1.jpg')
im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

lower_blue, upper_blue = getHsvThreshold([91, 155, 213])
mask = cv2.inRange(im_hsv, lower_blue, upper_blue)
blur=cv2.medianBlur(mask,5)

# opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

ret,thresh = cv2.threshold(blur,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# # raise exception if grid is different
# if hierarchy.max() != 6:
#     # #DEBUG
#     cv2.drawContours(im, contours, -1, (0,255,0), 50)
#     cv2.imwrite('mask.jpg', blur)
#     viewPage(mask)
#     viewPage(blur)
#     print(cv2.contourArea(contours[0]))
#     print('Does not have 7 contours (%s)' % hierarchy.max())
#     # #DEBUG END
#     raise Exception('Does not have 7 contours (%s)' % hierarchy.max())
# # print(hierarchy)

# debugcnt(contours[1],cv2.imread('cache/1.jpg'))


idx=0
for cnt in contours:
    idx += 1
    if cv2.contourArea(cnt)>62000 and cv2.contourArea(cnt)<63000:
        im3 = cv2.imread('cache/1.jpg')
        x, y, w, h = cv2.boundingRect(cnt)
        roi = im3[y:y + h, x:x + w]

        roigray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        ret, dateimg = cv2.threshold(roigray, 127, 255, 0)

        kernel = np.ones((3, 3), np.uint8)
        dateimg = cv2.morphologyEx(dateimg, cv2.MORPH_OPEN, kernel)


        datestr=pytesseract.image_to_string(Image.fromarray(dateimg), lang="number", config='-psm 6 -classify_bln_numeric_mode 1')
        # viewPage(dateimg,datestr)
        # cv2.imwrite('cache/temp/%s.jpg' % (idx-1), dateimg)
        cv2.imwrite('cache/temp/%s.jpg' % datestr, dateimg)


        # #DEBUG
        # cv2.drawContours(im3, [cnt], -1, (0, 255, 0), 50)
        # viewPage(im3)
        # #DEBUG END

