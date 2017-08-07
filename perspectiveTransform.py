import cv2, numpy
from func import *

def d3(points):
    point3D = []
    for point in points:
        point3D.append([point[0], point[1], 1])
    point3D = numpy.transpose(point3D)
    return point3D

structures = [{'page': [-0.5357142857142857, -0.37857142857142856, 25.057142857142857, 17.72142857142857], 'edge': [-0.02857142857142857, -0.02857142857142857, 16.707142857142856, 23.942857142857143], '2': [-0.014285714285714285, 4.414285714285715, 4.2, 19.478571428571428], '1': [4.2, 4.414285714285715, 12.457142857142857, 19.478571428571428], '4': [13.242857142857142, -0.007142857142857143, 3.414285714285714, 1.0214285714285714], '6': [-0.014285714285714285, -0.007142857142857143, 4.207142857142857, 1.0214285714285714], '3': [-0.014285714285714285, 1.0285714285714285, 16.67142857142857, 3.3714285714285714], 'QR': [0.0, 0.0, 1.0, 1.0], '5': [4.2, -0.007142857142857143, 9.028571428571428, 1.0214285714285714]}, {'8': [-74.0, -53.0, -588.0, -3390.0], 'page': [-1.0, -1.0, -3508.0, -2481.0], 'edge': [-72.0, -50.0, -2339.0, -3396.0], 'QR': [-0.0, -0.0, 1.0, 1.0], '7': [-664.0, -53.0, -1744.0, -3390.0]}]

page=cv2.imread('cache/t6.jpg')
page=cv2.cvtColor(page,cv2.COLOR_BGR2GRAY)
QR=findQR(page.copy())[0]
x,y,w,h=structures[0]["QR"]
xc, yc, wc, hc = locateQR(page.copy(), returnArray=0)  # x (QR)code, y (QR)code
x, y, w, h = [int(x * wc) + xc, int(y * hc) + yc, int(w * wc), int(h * hc)]

points=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]  #tl, tr, br, bl

print(points)

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
M,QRimg=four_point_transform(page,numpy.array(QR.position),returnMatrix=1)

# print(QR)
viewPage(QRimg)

QR2=findQR(QRimg)[0]
cv2.imwrite('xxx.jpg',QRimg)
# print(numpy.array(order_points(QR.position)))



h, status = cv2.findHomography(numpy.array(QR.position))

# print(h)
# print(M)
x= np.dot(h,d3(QR.position))
y= np.dot(h,d3(QR2.position))

print(x)
print(y)

print


