import sqlite3
import cv2, numpy
import json

from func import *

conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()


# future  perspective transformation
page=cv2.imread('cache/t14.jpg')
# page=cv2.imread('cache/page--0.jpg')


# get QR from correct orientate file what only contain page

pageGray=cv2.cvtColor(page,cv2.COLOR_BGR2GRAY)
for qr in findQR(pageGray):
    try:
        name,version,count=qr.data.decode().split(":")
        loc=qr.position
        pageQR=qr
        xc, yc, wc, hc = [loc[0][0], loc[0][1], loc[3][0] - loc[0][0], loc[2][1] - loc[0][1]]
    except ValueError:
        pass
# # debug:
# name,version,count=["note_alt",0,1]
# xc, yc, wc, hc = locateQR(pageGray.copy(), returnArray=0)  # x (QR)code, y (QR)code
# # end debug

# [{"note": [-2.996523754345307, 1.0579374275782156, 4.040556199304751, 6.31981460023175], "sub-heading": [-2.9976825028968714, -0.37543453070683663, 2.9281575898030128, 0.3302433371958285], "QR": [0.0, 0.0, 1.0, 1.0], "summary": [-4.363847045191194, -0.039397450753186555, 5.407879490150638, 1.0915411355735805], "edge": [-4.369640787949015, -0.3823870220162225, 5.420625724217845, 7.767091541135573], "page": [-4.534183082271147, -0.49710312862108924, 5.748551564310545, 8.129779837775203], "heading": [-4.363847045191194, -0.37543453070683663, 1.3626882966396292, 0.3302433371958285], "date": [-0.06373117033603708, -0.37543453070683663, 1.1077636152954808, 0.3302433371958285], "key": [-4.363847045191194, 1.0579374275782156, 1.361529548088065, 6.31981460023175]}, {"note": [-1328.0, -106.0, -3487.0, -6778.0], "edge": [-143.0, -100.0, -4678.0, -6790.0], "page": [-1.0, -1.0, -4961.0, -7016.0], "QR": [-0.0, -0.0, 1.0, 1.0], "key": [-148.0, -106.0, -1175.0, -6778.0]}]
try:
    structureStr,mode = c.execute('SELECT `layout`,`mode` FROM templates WHERE `name`=? and version=?',[name,version]).fetchall()[0]
    structures=json.loads(structureStr)
except (NameError,IndexError):
    raise Exception("unable to find structure info about this page from DB")


hp, wp,Chanel = page.shape  # hp height of page, wp width of page


# Convert structures from ratio to absolute
if mode==0:
    for name, part in structures[0].items(): # 0 for 1st page, alt later
        x, y, w, h = part
        structures[0][name] = [int(x * wp), int(y * hp), int(w * wp), int(h * hp)]

        # # debug start
        # page2=page.copy()  # one at time
        # # page2=page  # show all section
        # x, y, w, h = structures[0][name]
        # cv2.rectangle(page2, (x, y), (x + w, y + h), (0, 255, 0), 5)
        # cv2.putText(page2,name,(x, y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX,5,(0,255,0),20)
        # print(name)
        # print(part)
        # print([x, y, w, h])
        # print("\n")
        # viewPage(page2, resizeFactor=0.175)
        # # debug end

        # ocr debug
        x, y, w, h = structures[0][name]
        page2=page.copy()  # one at time
        roi = page2[y:y + h, x:x + w]
        cv2.imwrite('cache/ocr/%s.jpg'% name,roi)
elif mode==1:
    raise Exception("unable to find counter")
elif mode==2:
    for name, part in structures[0].items(): # 0 for 1st page, alt later
        x,y,w,h=part
        structures[0][name]=[int(x*wc)+xc,int(y*hc)+yc,int(w*wc),int(h*hc)]

        # debug start
        page2=page.copy()  # one at time
        # page2=page  # show all section
        x,y,w,h= structures[0][name]
        cv2.rectangle(page2, (x, y), (x + w, y + h), (0, 255, 0), 5)
        cv2.putText(page2,name,(x, y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX,5,(0,255,0),10)
        print(name)
        print(part)
        print([x,y,w,h])
        print("\n")
        viewPage(page2,resizeFactor=0.175)
        # debug end
else:
    raise Exception("error")

print(structures)


# read info from page
x,y,w,h=structures[0]["date"]
date=img2date(pageGray[y:y+h,x:x+w])

x,y,w,h=structures[0]["heading"]
heading=img2str(pageGray[y:y+h,x:x+w])

# data to ne stored
subject="eng"  # later ask for type(class) and subject. At last use heading to find subject
data=[pageQR.data.decode(),subject,]  # QRcode, subject, heading, sub-heading, summary, date
