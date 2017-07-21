import qrcode
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,cm



def getQR(jsonData,size,):
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
# jsonData = '{"7d529dd4-548b-4258-aa8e-23e34dc8d43d":99999999999}'
# img=getQR(jsonData,50)
# with open('QRtest.png', 'wb') as f:
#     img.save(f)


packet = BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=A4)
can.drawString(10, 100, "Hello world")
can.drawImage('QRtest.png',0*cm,0*cm,5*cm,5*cm,)
can.save()
#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("note.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()