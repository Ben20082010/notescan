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

print(img2date(imgray))


