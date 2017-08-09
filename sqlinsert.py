import sqlite3
import json

structures =[{'4': [-0.06264501160092807, -0.37587006960556846, 1.1090487238979119, 0.33178654292343385], 'page': [-4.538283062645012, -0.4965197215777262, 5.756380510440835, 8.139211136890951], 'edge': [-4.373549883990719, -0.382830626450116, 5.426914153132251, 7.7772621809744775], 'QR': [0.0, 0.0, 1.0, 1.0], '1': [-3.0, 1.060324825986079, 4.046403712296984, 6.327146171693736], '6': [-4.368909512761021, -0.37587006960556846, 1.3665893271461718, 0.33178654292343385], '5': [-3.0, -0.37587006960556846, 2.9327146171693736, 0.33178654292343385], '2': [-4.368909512761021, 1.060324825986079, 1.3642691415313226, 6.327146171693736], '3': [-4.368909512761021, -0.03944315545243619, 5.4153132250580045, 1.0951276102088168]}, {'page': [-1.0, -1.0, -2481.0, -3508.0], 'edge': [-72.0, -50.0, -2339.0, -3396.0], '7': [-664.0, -53.0, -1744.0, -3390.0], 'QR': [-0.0, -0.0, 1.0, 1.0], '8': [-74.0, -53.0, -588.0, -3390.0]}]

conn = sqlite3.connect('file:template/template.db', uri=True)
c = conn.cursor()

insertTemplate=[
    "note_alt",
    0,  #need change later
    0,
    json.dumps(structures),
    2
]  # name, version, count, layout, mode


templates=c.execute('SELECT `name`,`version` FROM templates WHERE `name`=? ORDER by `version` DESC', [insertTemplate[0]]).fetchall()

if len(templates)==0:
    c.execute('INSERT INTO templates VALUES (?,?,?,?,?)', insertTemplate)
else:
    print("template name exist")
    while True:
        command=input("Do you wish to [C]ancel or make [n]ew version?")
        # command=input("do you wish to [C]ancel or make [n]ew version or [R]place?")
        if command=="C":
            break
        elif command=="n":
            insertTemplate[1]=templates[0][1]+1 # +1 version number
            c.execute('INSERT INTO templates VALUES (?,?,?,?,?)', insertTemplate)
            break

conn.commit()
conn.close()



# try:
#
# except sqlite3.IntegrityError as e:
#     if e.__str__().find('UNIQUE constraint') > -1:
#         print(e)
#     else:
#         raise Exception(e)

