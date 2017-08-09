import cv2, numpy
import json
import sqlite3
import shutil

from wand.image import Image as Im
from PIL import Image

from func import *

# templatePath= 'template/note_alt.pdf'
# templatePath= 'destination.pdf'
# templatePath= 'template/note.pdf'
templatePath=input("location of PDF relative to this py file")

im = Im(filename=templatePath, resolution=600)
structures=[]

### get input of mode val
mode = input("mode?")
print(mode)

for i, page in enumerate(im.sequence):
    structure = {}

    ##### load template
    with Im(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='cache/page%s.jpg' % i)
        # to be improved
    page = cv2.imread('cache/page%s.jpg' % i)
    # page = cv2.imread('cache/temp/1.jpg')

    ##process img, find contours
    page_hsv = cv2.cvtColor(page, cv2.COLOR_BGR2HSV)
    page_gray = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)

    lower_blue, upper_blue = getHsvThreshold([91, 155, 213])  # user input
    mask = cv2.inRange(page_hsv, lower_blue, upper_blue)
    blur = cv2.medianBlur(mask, 5)
    ret, thresh = cv2.threshold(blur, 127, 255, 0)
    imMask, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    ## determine if is correct format ie: only  1 "2-level hierarchy"
    currentHrc=hierarchy[0][0] #[Next, Previous, First_Child, Parent]
    if currentHrc[0]>=0 or currentHrc[1]>=0:
        if currentHrc[3]<0:
            raise Exception('Have more than one "2-level hierarchy" on page%s of file named %s' % (i, templatePath))
        else:
            raise Exception('contour0 is not 1st level of "2-level hierarchy"')

    ##### find section (assume mode!=0, =1)
    idx = 0
    cntId=currentHrc[2]
    # print(contours[0])


    # # convert xywh to ratio with respect to page or 1st level of "2-level hierarchy"
    # for cnt in contours:
    #     x,y,w,h =cv2.boundingRect(cnt)
    # xs, ys, ws, hs = contours[0, 3]
    # if mode == 0:  # false include border, respect to page
    #     ratios = [xs / wp, ys / hp, ws / wp, hs / hp]
    # else:  # true respect to 1st level of "2-level hierarchy"
    #     ratios = [(xs - xf) / wf, (ys - yf) / hf, ws / wf, hs / hf]

    hp, wp, channels = page.shape  # hp height of page, wp width of page
    xf, yf, wf, hf = cv2.boundingRect(contours[0])  # x father cnt, y father cnt ...

    xc, yc, wc, hc = locateQR(page_gray.copy(), returnArray=0)  # x (QR)code, y (QR)code
    fixedItems={"page":[0,0,wp,hp],"edge":[xf, yf, wf, hf],"QR":[xc, yc, wc, hc]}
    for item,xyhw in fixedItems.items():
        x,y,w,h=xyhw
        if mode == '0':  # false include border, respect to page
            ratios = [x / w, y / hp, w / wp, h / hp]
        elif mode == '1':  # ref to 1st level of "2-level hierarchy
            ratios = [(x - xf) / wf, (y - yf) / hf, w / wf, h / hf]
        elif mode == '2':  # ref to QR code
            ratios = [(x - xc) / wc, (y - yc) / hc, w / wc, h / hc]
        else:
            raise Exception('mode not specified')
        structure[item] = ratios

    while True:
        cnt=contours[cntId]

        # process cnt2img
        idx += 1
        im3 = page.copy()
        x, y, w, h = cv2.boundingRect(cnt)
        roi = cropImg(im3, cv2.boundingRect(cnt))
        # cv2.imwrite('cache/temp/%s.jpg' % idx, roi)
        cv2.drawContours(im3, [cnt], -1, (0, 255, 0), 50)
        # viewPage(im3)

        if mode == '0':  # false include border, respect to page
            ratios = [x/w, y/hp, w/wp, h/hp]
        elif mode == '1': # ref to 1st level of "2-level hierarchy
            ratios = [(x - xf) / wf, (y - yf) / hf, w / wf, h / hf]
        elif mode =='2': # ref to QR code
            ratios=[(x - xc) / wc, (y - yc) / hc, w / wc, h / hc]

        name=input("name?")
        structure[name]=ratios

        # check if reached last where cntId is the id for next cnt
        cntId=hierarchy[0][cntId][0]
        if cntId<0:
            break
    structures.append(structure)
    print(structure)


print(structures)

## update to db
conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()

insertTemplate=[
    input("template name?"),
    0,  #need change later
    0,
    json.dumps(structures),
    2
]  # name, templateVersion, count, layout, mode


templates=c.execute('SELECT `name`,`templateVersion` FROM templates WHERE `name`=? ORDER by `templateVersion` DESC', [insertTemplate[0]]).fetchall()

if len(templates)==0:
    c.execute('INSERT INTO templates VALUES (?,?,?,?,?)', insertTemplate)
else:
    print("template name exist")
    while True:
        command=input("Do you wish to [C]ancel or make [n]ew templateVersion?")
        # command=input("do you wish to [C]ancel or make [n]ew templateVersion or [R]place?")
        if command=="C":
            break
        elif command=="n":
            insertTemplate[1]=templates[0][1]+1 # +1 templateVersion number
            c.execute('INSERT INTO templates VALUES (?,?,?,?,?)', insertTemplate)
            break

conn.commit()
conn.close()

shutil.copyfile(templatePath,'template/%s:%s' % (insertTemplate[0],insertTemplate[1]))