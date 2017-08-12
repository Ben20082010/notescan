# import sqlite3
#
# conn = sqlite3.connect('file:template/template.db', uri=True)
# c = conn.cursor()
#
# structure,mode = c.execute('SELECT `layout`,`mode` FROM templates WHERE `name`=? and version=?', ["note_alt", 0]).fetchall()[0]
#
# print(structure)
# print(mode)

from PIL import Image,ImageDraw

img = Image.new('RGBA', (600, 600))  ####
draw = ImageDraw.Draw(img)
draw.ellipse((0, 0, 600, 600), fill=(255, 255, 255, 255))  # white outline
draw.ellipse((50, 50, 550, 550), fill=(0, 0, 255, 255))  # circle core
draw.ellipse((281, 281, 318, 318), fill=(255, 0, 0, 255))  # point
img = img.transpose(Image.FLIP_TOP_BOTTOM)
with open('chicle.png', 'wb') as f:
    img.save(f)