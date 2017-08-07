import cv2,numpy as np
import zbar
import qrcode


# ## Open CV
def viewPage(image):
    cv2.imshow('view', image)
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


# the function order_points and four_point_transform are from
# http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

def four_point_transform(image, pts,returnMatrix=0):
    # obtain a consistent order of the points and unpack them individually
    # rect = order_points(pts)
    # (tl, tr, br, bl) = rect  # top-left, top-right, bottom-right, and bottom-left

    tl, bl, br, tr = pts
    rect=np.array([tl, tr, br, bl], dtype="float32")


    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    if returnMatrix==0:
        return warped
    else:
        return [M,warped]

# ## QR
def genQR(jsonData):
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

def findQR(npGrayImg):
    scanner = zbar.Scanner()
    return scanner.scan(npGrayImg)

def locateQR(npGrayImg,CodeData=None,CodeType='QR-Code',returnArray=0,):
    results = findQR(npGrayImg)

    if CodeData != None:
        for result in results:  ### edit 1 pre list pre page
            if result.data.decode() != CodeData : results.remove(result)

    if CodeType != None:
        for result in results:
            if result.type != CodeType : results.remove(result)

    print(results)
    if returnArray==0:
        if len(results) == 1:
            print(results)
            loc = results[0].position
            # in reportlab canvas start from bottom right coiner
            raw_xywh = [loc[0][0], loc[0][1], loc[3][0] - loc[0][0], loc[2][1] - loc[0][1]]
            return raw_xywh
        elif len(results)==0:
            return [-1,-1,-1,-1]
        else:
            raise Exception("more than 1 QR list")
    else:
        raw_xywhs=[]
        for result in results:
            loc = results[0].position
            # in reportlab canvas start from bottom right coiner
            raw_xywh = [loc[0][0], loc[0][1], loc[3][0] - loc[0][0], loc[2][1] - loc[0][1]]
            raw_xywhs.append(raw_xywh)
        return raw_xywhs



### unit conversion

