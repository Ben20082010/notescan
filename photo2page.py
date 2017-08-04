import cv2, numpy
from PIL import Image
from matplotlib import pyplot as plt


def viewPage(image):
    view=cv2.resize(image, (0,0), fx=0.35, fy=0.35)
    cv2.imshow('view', view)
    cv2.waitKey()


org = cv2.imread('cache/p3.jpg')
org = cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)

edges=cv2.Canny(org,100,200)

plt.subplot(121),plt.imshow(org,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()


# imgray = cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,200,255,0)
# im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(org, contours, -1, (0,255,0), 3)
# viewPage(thresh)
