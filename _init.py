import sqlite3


# init DB
# name => name of template eg note
# version => version of template
# count => count of print generated
# layout => jason form of layout of page eg {qr:[x,y,w,h],date:[x,y,w,h],title:[x,y,w,h]}
#   where [x,y,w,h] are ratio of length start from top-left side
#   when internal!=0 (ie true):
#       start from top-left conner of hierarchy-0 contour
#       ratio for x,w is x-coordinateFromConner/widthOfContour, widthOfInterest/widthOfContour
#       ratio for y,h is y-coordinateFromConner/heightOfContour, heightOfInterest/heightOfContour
#   when internal==0 (ie false):
#       start from top-left conner of page
#       ratio for x,w is x-coordinate/widthOfPage, widthOfInterest/widthOfPage
#       ratio for y,h is x-coordinate/heightOfPage, heightOfInterest/heightOfPage
# internal => true means crop image to hierarchy-0 contour then process, false means start process image from raw paper
#
conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()
c.execute('''CREATE TABLE templates (name text NOT NULL , version int NOT NULL , count int DEFAULT 0, layout text, internal int DEFAULT 0, PRIMARY KEY ( name, version)   )''')