import zbar
from PIL import Image
import cv2
import numpy


im=cv2.imread('cache/t2.jpg')
image=cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

scanner=zbar.Scanner()

results=scanner.scan(image)

print(results)

for result in results:
    print(1)
    print(result.type, result.data, result.quality, result.position)
