import cv2, numpy
import json

from func import *
structures = [{'page': [-0.5357142857142857, -0.37857142857142856, 25.057142857142857, 17.72142857142857], 'edge': [-0.02857142857142857, -0.02857142857142857, 16.707142857142856, 23.942857142857143], '2': [-0.014285714285714285, 4.414285714285715, 4.2, 19.478571428571428], '1': [4.2, 4.414285714285715, 12.457142857142857, 19.478571428571428], '4': [13.242857142857142, -0.007142857142857143, 3.414285714285714, 1.0214285714285714], '6': [-0.014285714285714285, -0.007142857142857143, 4.207142857142857, 1.0214285714285714], '3': [-0.014285714285714285, 1.0285714285714285, 16.67142857142857, 3.3714285714285714], 'QR': [0.0, 0.0, 1.0, 1.0], '5': [4.2, -0.007142857142857143, 9.028571428571428, 1.0214285714285714]}, {'8': [-74.0, -53.0, -588.0, -3390.0], 'page': [-1.0, -1.0, -3508.0, -2481.0], 'edge': [-72.0, -50.0, -2339.0, -3396.0], 'QR': [-0.0, -0.0, 1.0, 1.0], '7': [-664.0, -53.0, -1744.0, -3390.0]}]


page=cv2.imread('cache/t2.jpg')
# page=cv2.imread('cache/page-0.jpg')


xc, yc, wc, hc = locateQR(page.copy(), returnArray=0)  # x (QR)code, y (QR)code
hp, wp, channels = page.shape  # hp height of page, wp width of page

print([xc, yc, wc, hc ])
for name, part in structures[0].items():
    x,y,w,h=part


    # position=[int(x*wc)+xc,int(y*hc)+yc,int(w*wc),int(h*hc)]
    # crop=cropImg(page,position)
    # viewPage(crop)

    page2=page.copy()
    x,y,w,h=[int(x*wc)+xc,int(y*hc)+yc,int(w*wc),int(h*hc)]
    cv2.rectangle(page2, (x, y), (x + w, y + h), (0, 255, 0), 5)

    print(name)
    print(part)
    print([x,y,w,h])
    print("\n")
    viewPage(page2)
