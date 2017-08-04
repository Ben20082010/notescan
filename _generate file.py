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
jsonData = '{"7d529dd4-548b-4258-aa8e-23e34dc8d43d":99999999999}'
img=genQR(jsonData,50)
with open('QRtest.png', 'wb') as f:
    img.save(f)

# def genPage(id,idx):

# input
start = 1 # from sqlite
# number = input("number of pages to print?")
templatePath="template/note.pdf"

# ##get locations QR code
codeLists=[]
im = Im(filename=templatePath, resolution=300)
for i, page in enumerate(im.sequence):
    codeList=[]
    with Im(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='cache/page-%s.jpg' % i)
        # to be improved
    pageImg = cv2.imread('cache/page-%s.jpg' % i)
    image = cv2.cvtColor(pageImg, cv2.COLOR_BGR2GRAY)
    height, width=image.shape
    results=findQR(image)
    for result in results:
        if result.type=='QR-Code' and result.data.decode()=="pageid":
            loc=result.position
            # in reportlab canvas start from bottom right coiner
            xywh=numpy.array([loc[0][0],loc[0][1],loc[3][0]-loc[0][0],loc[2][1]-loc[0][1]])
            xywh=numpy.round(xywh/width*21,3)
            codeList.append(xywh)
    codeLists.append(codeList)

# ##plot pdf
# ##genearte all QR code on new page
packet = BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=A4,bottomup=0)
for codeList in codeLists:
    for xywh in codeList:
        can.drawImage('QRtest.png', xywh[0] * cm, xywh[1] * cm, xywh[2] * cm, xywh[3] * cm, )
    can.showPage()
can.save()
packet.seek(0) #move to the beginning of the StringIO buffer
# 2input & 1output
new_pdf = PdfFileReader(packet)
template = PdfFileReader(open(templatePath, "rb"))
output = PdfFileWriter()
# merge
for i in range(template.getNumPages()):
    page = template.getPage(i)
    page.mergePage(new_pdf.getPage(i))
    output.addPage(page)
# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()