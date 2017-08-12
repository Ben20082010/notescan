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

def findCircle(cnts,tolerance=0.20):
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
# path='cache/pagexxx.png'
path='cache/t18.jpg'


# path='cache/page-0.jpg'
# path='cache/t15.jpg'

structures=[{"note":[0.2533133817870885,0.1854393555124571,0.7454040188114579,0.8136655229001939],"key":[0.0010688328345446773,0.1854393555124571,0.25117571611799916,0.8136655229001939],"summary":[0.0010688328345446773,0.044159331642548115,0.9976485677640017,0.14053408921378488],"date":[0.7943565626336041,0.0008951215873489483,0.20436083796494228,0.04251827539907504],"sub-heading":[0.25309961522017954,0.0008951215873489483,0.5401881145788798,0.04251827539907504],"heading":[0.0010688328345446773,0.0008951215873489483,0.25138948268490807,0.04251827539907504],"edge":[0,0,1,1],"page":[-0.030354852501068834,-0.014769506191257645,1.0604959384352288,1.04669550947337],"QR":[0.8061137238135956,0.049231687304192154,0.18448054724241128,0.1287483216470237]},{"note":[0.0010688328345446773,0.0008836524300441826,0.25117571611799916,0.9982326951399116],"edge":[0,0,1,1],"page":[-0.030354852501068834,-0.014580265095729013,1.0604959384352288,1.0332842415316643],"QR":[-0.030568619067977768,-0.014727540500736377,-0.00021376656690893543,-0.00014727540500736376]}]

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

# viewPage(im)
# # viewPage(mask)
# viewPage(blur)


xyrs=findCircle(contours)
xyrs=np.array(xyrs).astype(int)
# for xyr in xyrs:
#     x,y,r=xyr
#     cv2.circle(im,(x,y),r,(0,0,255),5)

# # Perspective Transformation
xys=np.delete(xyrs, -1, axis=1)

corrected=four_point_transform(im,xys)

# plt.subplot(121),plt.imshow(im),plt.title('Input')
# plt.subplot(122),plt.imshow(corrected),plt.title('Output')
# plt.show()


hf, wf, channels = corrected.shape
for name, part in structures[0].items():  # 0 for 1st page, alt later
    x, y, w, h = part
    structures[0][name] = [int(x * wf), int(y * hf), int(w * wf), int(h * hf)]

    # debug start
    page2 = corrected.copy()  # one at time
    # page2=page  # show all section
    x, y, w, h = structures[0][name]
    cv2.rectangle(page2, (x, y), (x + w, y + h), (0, 255, 0), 5)
    cv2.putText(page2, name, (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 20)
    print(name)
    print(part)
    print([x, y, w, h])
    print("\n")
    viewPage(page2,resizeFactor=0.4)
    # debug end

    # # ocr debug
    # x, y, w, h = structures[0][name]
    # page2 = page.copy()  # one at time
    # roi = pageGray[y:y + h, x:x + w]
    # ret, dateimg = cv2.threshold(roi, 100, 255, 0)
    # cv2.imwrite('cache/ocr/%s.jpg' % name, dateimg)

cv2.imwrite('cache/p0.jpg',corrected)


