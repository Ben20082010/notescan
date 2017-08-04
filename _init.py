import sqlite3


# init DB
# name => name of template eg note
# version => version of template
# count => count of print generated
# layout => jason form of layout of pages eg [{qr:[x,y,w,h],date:[x,y,w,h],title:[x,y,w,h]}, {qr:[x,y,w,h],date:[x,y,w,h],title:[x,y,w,h]}]  <== [page1,page2]
#   where [x,y,w,h] are ratio of length start from top-left side
#   when internal!=0 (ie true):
#       start from top-left conner of hierarchy-0 contour
#       ratio for x,w is x-coordinateOfSectionFromConner/widthOfContour, widthOfSection/widthOfContour
#       ratio for y,h is y-coordinateOfSectionFromConner/heightOfContour, heightOfSection/heightOfContour
#   when internal==0 (ie false):
#       start from top-left conner of page
#       ratio for x,w is x-coordinateOfSection/widthOfPage, widthOfSection/widthOfPage
#       ratio for y,h is x-coordinateOfSection/heightOfPage, heightOfSection/heightOfPage
# internal => true means crop image to hierarchy-0 contour then process, false means start process image from raw paper
#
conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()
c.execute('''CREATE TABLE templates (name text NOT NULL , version int NOT NULL , count int DEFAULT 0, layout text, internal int DEFAULT 0, PRIMARY KEY ( name, version)   )''')