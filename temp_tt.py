import sqlite3

conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()

structure,mode = c.execute('SELECT `layout`,`mode` FROM templates WHERE `name`=? and version=?', ["note_alt", 0]).fetchall()[0]

print(structure)
print(mode)