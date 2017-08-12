import cv2,numpy as np
import zbar
import qrcode
import datetime
import pytesseract

from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,cm
from reportlab.graphics.shapes import Circle
from PIL import Image,ImageDraw
from wand.image import Image as Im


from wand.image import Image as Im

# ## PDF
def pdf2img(pdfPath,resolution=600):
    im = Im(filename=pdfPath, resolution=resolution)
    imgs=[]
    for i, page in enumerate(im.sequence):
        with Image(page) as page_image:
            page_image.alpha_channel = False
            page_image.save(filename='cache/page-%s.jpg' % i)
            imgs.append('cache/page-%s.jpg' % i)
    return imgs


# ## Open CV
def viewPage(image,resizeFactor=1):
    # 300 => 0.35
    # 600 => 0.175
    image = cv2.resize(image, (0, 0), fx=resizeFactor, fy=resizeFactor)
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

# def four_point_transform(image, pts, recover, returnMatrix=0):
def four_point_transform(image, pts, returnMatrix=0):

    # obtain a consistent order of the points and unpack them individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect  # top-left, top-right, bottom-right, and bottom-left

    # tl, bl, br, tr = pts
    # rect=np.array([tl, tr, br, bl], dtype="float32")


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
    #
    # make top-right size of page as 0,0

    # xp,yp,wp,hp=recover  # with respect to QR code (ratio)
    # xp=xp*maxWidth  # covert to value from ratio (page from QR)
    # wp=wp*maxWidth
    # yp=yp*maxHeight
    # hp=hp*maxHeight

    #change to QR from page

    # pattern found by represent as vector
    # (a,b) where a=xp, b=yp, c=xp+maxWidth, d=yp+maxHeight when use QR as reference
    # (c,b) where a=xp, b=yp, c=xp+maxWidth, d=yp+maxHeight when use QR as reference
    # (c,d) where a=xp, b=yp, c=xp+maxWidth, d=yp+maxHeight when use QR as reference
    # (a,d) where a=xp, b=yp, c=xp+maxWidth, d=yp+maxHeight when use QR as reference
    # dst = np.array([
    #     [-xp-1, -yp-1],
    #     [-xp+maxWidth - 1, -yp-1],
    #     [-xp+maxWidth - 1, -yp+maxHeight - 1],
    #     [-xp-1, -yp+maxHeight - 1]], dtype="float32")

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    # warped = cv2.warpPerspective(image, M,(int(wp),int(hp)))
    warped = cv2.warpPerspective(image, M,(int(maxWidth),int(maxHeight)))


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
            # only use loc0,1,3 as they are accurate
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

def addQR2Template(templatePath,output, QRstr, xywhs):  #xywhs unit here is cm
    img = genQR(QRstr)  ####
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    with open('%s.png' % QRstr, 'wb') as f:
        img.save(f)

    # gen pdf
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4, bottomup=0)

    for xywh in xywhs:
        can.drawImage('%s.png' % QRstr, xywh[0] * cm, xywh[1] * cm, xywh[2] * cm, xywh[3] * cm, )
        can.showPage()
    can.save()
    # packet.seek(0) #move to the beginning of the StringIO buffer
    # 2input & 1output
    new_pdf = PdfFileReader(packet)
    # merge
    template = PdfFileReader(open(templatePath, "rb"))
    for i in range(template.getNumPages()):
        page = template.getPage(i)
        try:
            page.mergePage(new_pdf.getPage(i))
        except IndexError:
            pass
        output.addPage(page)


def addCircle2Template(inputPath, output, radius, xyses):  # xyses is [xys, xys]; where xys is [xy,xy];  unit here is cm
    img = Image.new('RGBA', (600, 600))  ####
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, 600, 600), fill=(255, 255, 255, 255))  # white outline
    draw.ellipse((50, 50, 550, 550), fill=(0, 0, 255, 255))  # circle core
    draw.ellipse((281, 281, 318, 318), fill=(255, 0, 0, 255))  # point
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    with open('chicle.png', 'wb') as f:
        img.save(f)


    # gen pdf
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4, bottomup=0)

    for xys in xyses:
        for xy in xys:
            can.drawImage('chicle.png', (xy[0]-radius) * cm, (xy[1]-radius) * cm, (radius*2) * cm, (radius*2) * cm, mask='auto')
        can.showPage()
    can.save()


    # packet.seek(0) #move to the beginning of the StringIO buffer
    # 2input & 1output
    new_pdf = PdfFileReader(packet)
    # merge
    input = PdfFileReader(open(inputPath, "rb"))
    for i in range(input.getNumPages()):
        page = input.getPage(i)
        try:
            page.mergePage(new_pdf.getPage(i))
        except IndexError:
            pass
        output.addPage(page)

# ## date conversion
def validateDate(dateStr):
    try:
        D,M,Y=list(filter(None, dateStr.split(" ")))
        date = datetime.datetime(int(Y), int(M), int(D))
        #  ##more compare in the further
        # if D>31:
        #     raise Exception("day(%s) greater than 31",D)
        # if M>12:
        #     raise Exception("month(%s) greater than 12",M)
    except ValueError:
        raise Exception("Date format not correct")
    return date

def img2date(imgGray):
    ret, dateimg = cv2.threshold(imgGray, 100, 255, 0)
    kernel = np.ones((3, 3), np.uint8)
    dateimg = cv2.morphologyEx(dateimg, cv2.MORPH_OPEN, kernel)
    datestr=pytesseract.image_to_string(Image.fromarray(dateimg), lang="number", config='-psm 6 -classify_bln_numeric_mode 1')
    print(datestr)
    return validateDate(datestr)

def img2strs(imgGray):
    ret, dateimg = cv2.threshold(imgGray, 127, 255, 0)

    kernel = np.ones((3, 3), np.uint8)
    strimg = cv2.morphologyEx(dateimg, cv2.MORPH_OPEN, kernel)

    strstr=pytesseract.image_to_string(Image.fromarray(strimg), lang="english", config='-psm 6 -l eng')

    return strstr

# ## input
def checkInput(inputstr,inputname=None,case=0):
    while True:
        str=input("Please check the %s is the following (press enter to confirm) \n %s \n" % (inputname,inputstr))
        if str=='':
            break
        else:
            inputstr = str

        if case > 0:
            inputstr=inputstr.upper()
            print("upper")
        elif case < 0:
            print("lower")
            inputstr=inputstr.lower()

    return inputstr

