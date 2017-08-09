import sqlite3


# init DB
# name => name of template eg note
# templateVersion => templateVersion of template
# count => count of print generated
# layout => jason form of layout of pages eg [{qr:[x,y,w,h],date:[x,y,w,h],title:[x,y,w,h]}, {qr:[x,y,w,h],date:[x,y,w,h],title:[x,y,w,h]}]  <== [page1,page2]
#   where [x,y,w,h] are ratio of length start from top-left side
#   when mode!=0:
#       start from top-left of the object and use its dimension as unit 1 for x,y independently
#       ratio for x,w is x-coordinateOfSectionFromConner/widthOfContour, widthOfSection/widthOfContour
#       ratio for y,h is y-coordinateOfSectionFromConner/heightOfContour, heightOfSection/heightOfContour
#   when mode==0 (ie false):
#       start from top-left conner of page
#       ratio for x,w is x-coordinateOfSection/widthOfPage, widthOfSection/widthOfPage
#       ratio for y,h is x-coordinateOfSection/heightOfPage, heightOfSection/heightOfPage
# mode => reference object for origin and base of size ratio
#   0 => start from top-left conner of page
#   1 => start from hierarchy-0 contour
#   2 => start from QR code, use its size as reference
#
conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()
# name, templateVersion, count, layout, mode
c.execute('''CREATE TABLE templates (name text NOT NULL , templateVersion int NOT NULL , count int DEFAULT 0, layout text, mode int DEFAULT 0, PRIMARY KEY ( name, templateVersion)   )''')