import zbar
from PIL import Image
import cv2
import numpy


im=cv2.imread('cache/page-0.jpg')
image=cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

scanner=zbar.Scanner()

results=scanner.scan(image)

print(results)

for result in results:
    print(1)
    print(result.type, result.data, result.quality, result.position)



# pil=Image.fromarray(QR)
# width,height = pil.size
# raw=pil.tobytes()
#
# image = zbar.Image(width, height, 'Y800', raw)
#
# scanner.scan(image)
#
# for symbol in image:
#             # do something useful with results
#             if symbol.data == "None":
#                 print( "Drone bevindt zich buiten het raster")
#             else:
#                 print( symbol.data)