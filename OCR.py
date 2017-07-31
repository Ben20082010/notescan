import pytesseract
import cv2
import numpy as np
from PIL import Image


# def img2string(image_path):
#     return pytesseract.image_to_string(Image.open(image_path),lang="eng")
#
# print(pytesseract.image_to_string(Image.open('z.png'), lang="eng"))
#
#     # pytesseract.image_to_string(Image.open('z.png'),lang="eng")



im = cv2.imread('y.png')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
cv2.imshow('view', thresh)
cv2.waitKey()
print(pytesseract.image_to_string(Image.fromarray(thresh), lang="eng"))