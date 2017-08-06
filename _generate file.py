import qrcode
import numpy
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,cm

from wand.image import Image as Im


from func import *

pagesize=[21,29.7]


# def genPage(id,idx):

# input
start = 10 + 1 # 10 from sqlite
numbers = int(input("number of pages to print?"))
templatePath="template/note.pdf"
templateName="7d529dd4-548b-4258-aa8e-23e34dc8d43d"

# ##get locations QR code
xywhs=[]
im = Im(filename=templatePath, resolution=300)
for i, page in enumerate(im.sequence):
    with Im(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='cache/page-%s.jpg' % i)
        # to be improved
    pageImg = cv2.imread('cache/page-%s.jpg' % i)

    height, width, channel = pageImg.shape
    raw_xywh=numpy.array(locateQR(pageImg,returnArray=0))
    xywh=numpy.round(raw_xywh / width * 21, 3)

    xywhs.append(xywh)

# ##plot pdf
# ##genearte all QR code on new page

# create a new PDF with Reportlab
output = PdfFileWriter()
outputStream = open("destination.pdf", "wb")
for num in range(start,start+numbers):

    #gen QR code
    print(num)
    img = genQR("%s:%s" % (templateName,num))
    with open('QR%s.png' % num, 'wb') as f:
        img.save(f)

    #gen pdf
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4,bottomup=0)
    for xywh in xywhs:
        can.drawImage('QR%s.png' % num, xywh[0] * cm, xywh[1] * cm, xywh[2] * cm, xywh[3] * cm, )
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

output.write(outputStream)
# finally, write "output" to a real file
outputStream.close()