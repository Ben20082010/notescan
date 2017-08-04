import cv2,numpy as np
import zbar
import qrcode

def viewPage(image):
    view=cv2.resize(image, (0,0), fx=0.35, fy=0.35)
    cv2.imshow('view', view)
    cv2.waitKey()


def getHsvThreshold(RGB):
    hsv = cv2.cvtColor(np.uint8([[RGB]]), cv2.COLOR_RGB2HSV)[0][0]

    # low=[hsv[0]-10,90,155 ]
    # high=[hsv[0]+10,160,224]

    low=[hsv[0]-10,40,100 ]
    high=[hsv[0]+10,160,255]
    return np.array(low), np.array(high)

def cropImg(img,position):
    x,y,w,h=position
    roi = img[y:y + h, x:x + w]
    return roi


# ## QR
def genQR(jsonData,size,):
    # BUG unreadable QR code if size to small
    # json format: {"name(code) of the note" : number}
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=0,
    )
    qr.add_data(jsonData)
    qr.make(fit=True)
    img = qr.make_image()
    # img = img.resize((size,size),Image.NEAREST)
    return img

def findQR(npImg):
    scanner = zbar.Scanner()
    results = scanner.scan(npImg)
    return scanner.scan(npImg)

### unit conversion

