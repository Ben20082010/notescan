import cv2, numpy
import json

from wand.image import Image as Im
from PIL import Image

from func import *

tempaltePath='template/note.pdf'

im = Im(filename=tempaltePath, resolution=300)
structures=[]

### get input of internal val
internal = input("internal?")
print(internal)

for i, page in enumerate(im.sequence):
    structure = {}

    ##### load template
    with Im(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='cache/page-%s.jpg' % i)
        # to be improved
    page = cv2.imread('cache/page-%s.jpg' % i)
    # page = cv2.imread('cache/temp/1.jpg')

    ##process img, find contours
    page_hsv = cv2.cvtColor(page, cv2.COLOR_BGR2HSV)

    lower_blue, upper_blue = getHsvThreshold([91, 155, 213])  # user input
    mask = cv2.inRange(page_hsv, lower_blue, upper_blue)
    blur = cv2.medianBlur(mask, 5)
    ret, thresh = cv2.threshold(blur, 127, 255, 0)
    imMask, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    ## determine if is correct format ie: only  1 "2-level hierarchy"
    currentHrc=hierarchy[0][0] #[Next, Previous, First_Child, Parent]
    if currentHrc[0]>=0 or currentHrc[1]>=0:
        if currentHrc[3]<0:
            raise Exception('Have more than one "2-level hierarchy" on page%s of file named %s' % (i, tempaltePath))
        else:
            raise Exception('contour0 is not 1st level of "2-level hierarchy"')

    ##### find section (assume internal!=0, =1)
    idx = 0
    cntId=currentHrc[2]

    while True:
        cnt=contours[cntId]

        idx += 1
        im3 = page.copy()
        # im3 = cv2.imread('cache/1.jpg')
        # x, y, w, h = cv2.boundingRect(cnt)
        # print(x, y, w, h)
        roi = cropImg(im3, cv2.boundingRect(cnt))
        cv2.imwrite('cache/temp/%s.jpg' % idx, roi)
        # DEBUG
        cv2.drawContours(im3, [cnt], -1, (0, 255, 0), 50)
        viewPage(im3)

        # check if reached last where cntId is the id for next cnt
        cntId=hierarchy[0][cntId][0]
        if cntId<0:
            break