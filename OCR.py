import pytesseract
import cv2
import numpy as np
from PIL import Image
import datetime

from func import *

# def img2string(image_path):
#     return pytesseract.image_to_string(Image.open(image_path),lang="eng")
#
# print(pytesseract.image_to_string(Image.open('z.png'), lang="eng"))
#
#     # pytesseract.image_to_string(Image.open('z.png'),lang="eng")




im = cv2.imread('cache/number train/date/2.jpg')

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

ret, dateimg = cv2.threshold(imgray, 127, 255, 0)

kernel = np.ones((3, 3), np.uint8)
dateimg = cv2.morphologyEx(dateimg, cv2.MORPH_OPEN, kernel)


datestr=pytesseract.image_to_string(Image.fromarray(dateimg), lang="number", config='-psm 6 -classify_bln_numeric_mode 1')

date=validateDate("20   9 2015")
print(date)


