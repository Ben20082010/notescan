import qrcode
import numpy
import sqlite3
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,cm

from wand.image import Image as Im


from func import *

conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()

pagesize=[21,29.7]


# def genPage(id,idx):

# input

templateName=input('name of template?')

templates=c.execute('SELECT `name`,`version`,`count` FROM templates WHERE `name`=? ORDER by `version` DESC',[templateName]).fetchall()
try:
    templateVersion=int(input("\nVersion of template (%s-%s) ?" % (templates[-1][1], templates[0][1])))
except ValueError:
    templateVersion = templates[0][1]
    print("invalid input, use latest version (%s)" % templateVersion)
findVersion=False
for template in templates:
    if templateVersion == template[1]:
        start = template[2]
        findVersion=True
        break
if findVersion == False: raise Exception("Version not exist in DB")

numbers = int(input("\nnumber of pages to print?"))



# templatePath="template/note.pdf"
# templatePath="template/note_alt.pdf"
templatePath="template/%s:%s" % (templateName, templateVersion)

# ##get locations QR code
xywhs=[]
im = Im(filename=templatePath, resolution=600)
for i, page in enumerate(im.sequence):
    with Im(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='cache/page-%s.jpg' % i)
        # to be improved
    pageImg = cv2.imread('cache/page-%s.jpg' % i)

    height, width, channel = pageImg.shape
    PageGray=cv2.cvtColor(pageImg,cv2.COLOR_BGR2GRAY)
    raw_xywh=numpy.array(locateQR(PageGray.copy(),returnArray=0))
    xywh=numpy.round(raw_xywh / width * 21, 3)

    xywhs.append(xywh)

# ##plot pdf
# ##genearte all QR code on new page

# create a new PDF with Reportlab
output = PdfFileWriter()

for num in range(start,start+numbers):
    #gen QR code
    print(num)
    QRStr="%s:%s.%s" % (templateName, templateVersion, num)
    addQR2Template(templatePath,output,QRStr,xywhs)



## update count before write to file
c.execute('UPDATE templates SET count = ? WHERE name=? and version=?', [start + numbers, templateName, templateVersion])
conn.commit()
conn.close()

## write to file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
# finally, write "output" to a real file
outputStream.close()


