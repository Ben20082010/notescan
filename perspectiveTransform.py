import cv2, numpy
from func import *

def d3(points):
    point3D = []
    for point in points:
        point3D.append([point[0], point[1], 1])
    point3D = numpy.transpose(point3D)
    return point3D
#note
# structures =[{'edge': [-0.02857142857142857, -0.02857142857142857, 16.707142857142856, 23.942857142857143], '3': [-0.014285714285714285, 1.0285714285714285, 16.67142857142857, 3.3714285714285714], 'page': [-0.5357142857142857, -0.37857142857142856, 17.72142857142857, 25.057142857142857], '5': [4.2, -0.007142857142857143, 9.028571428571428, 1.0214285714285714], '1': [4.2, 4.414285714285715, 12.457142857142857, 19.478571428571428], '2': [-0.014285714285714285, 4.414285714285715, 4.2, 19.478571428571428], '4': [13.242857142857142, -0.007142857142857143, 3.414285714285714, 1.0214285714285714], 'QR': [0.0, 0.0, 1.0, 1.0], '6': [-0.014285714285714285, -0.007142857142857143, 4.207142857142857, 1.0214285714285714]}, {'8': [-74.0, -53.0, -588.0, -3390.0], 'edge': [-72.0, -50.0, -2339.0, -3396.0], 'page': [-1.0, -1.0, -2481.0, -3508.0], '7': [-664.0, -53.0, -1744.0, -3390.0], 'QR': [-0.0, -0.0, 1.0, 1.0]}]

#note_alt
structures =[{'5': [-3.0, -0.37587006960556846, 2.9327146171693736, 0.33178654292343385], '1': [-3.0, 1.060324825986079, 4.046403712296984, 6.327146171693736], '3': [-4.368909512761021, -0.03944315545243619, 5.4153132250580045, 1.0951276102088168], '6': [-4.368909512761021, -0.37587006960556846, 1.3665893271461718, 0.33178654292343385], 'QR': [0.0, 0.0, 1.0, 1.0], '4': [-0.06264501160092807, -0.37587006960556846, 1.1090487238979119, 0.33178654292343385], '2': [-4.368909512761021, 1.060324825986079, 1.3642691415313226, 6.327146171693736], 'page': [-4.538283062645012, -0.4965197215777262, 5.756380510440835, 8.139211136890951], 'edge': [-4.373549883990719, -0.382830626450116, 5.426914153132251, 7.7772621809744775]}, {'8': [-74.0, -53.0, -588.0, -3390.0], '7': [-664.0, -53.0, -1744.0, -3390.0], 'page': [-1.0, -1.0, -2481.0, -3508.0], 'QR': [-0.0, -0.0, 1.0, 1.0], 'edge': [-72.0, -50.0, -2339.0, -3396.0]}]



# page=cv2.imread('cache/t2.jpg')
page=cv2.imread('cache/page_0.jpg')

pageGray=cv2.cvtColor(page,cv2.COLOR_BGR2GRAY)
QR=findQR(pageGray.copy())[0]
# x,y,w,h=structures[0]["QR"]
# xc, yc, wc, hc = locateQR(page.copy(), returnArray=0)  # x (QR)code, y (QR)code
# x, y, w, h = [int(x * wc) + xc, int(y * hc) + yc, int(w * wc), int(h * hc)]
#
# points=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]  #tl, tr, br, bl
#
# print(points)

# def click(event, x, y, flags, param):
#     # grab references to the global variables
#     global points
#
#     # if the left mouse button was clicked, record the starting
#     # (x, y) coordinates and indicate that cropping is being
#     # performed
#     if event == cv2.EVENT_LBUTTONDOWN:
#         point = (x, y)
#         points.append(point)
#         cv2.circle(page,point,5,(0,255,0),-1)
# # load the image, clone it, and setup the mouse callback function
# clone = page.copy()
# cv2.namedWindow("image")
# cv2.setMouseCallback("image", click)
#
# # keep looping until the 'q' key is pressed
# while True:
#     # display the image and wait for a keypress
#     cv2.imshow("image", page)
#     key = cv2.waitKey(1) & 0xFF
#
#     # if the 'r' key is pressed, reset the cropping region
#     if key == ord("r"):
#         image = clone.copy()
#
#     # if the 'c' key is pressed, break from the loop
#     elif key == ord("c"):
#         break
#
# # close all open windows
# cv2.destroyAllWindows()
# print(points)





# QRimg=four_point_transform(page,numpy.array(QR.position))
# QRimg=four_point_transform(page,numpy.array(points))
print(QR)
M,QRimg=four_point_transform(page,numpy.array(QR.position),structures[0]["page"],returnMatrix=1)

# print(QR)
viewPage(QRimg,resize=1)

QRGray=cv2.cvtColor(QRimg,cv2.COLOR_BGR2GRAY)
QR2=findQR(QRGray)[0]
cv2.imwrite('xxx.jpg',QRimg)
# print(numpy.array(order_points(QR.position)))



# h, status = cv2.findHomography(numpy.array(QR.position))




