import qrcode

# json format: {"name(code) of the note" : number}
jsonData = '{"7d529dd4-548b-4258-aa8e-23e34dc8d43d":99999999999}'
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=2,
    border=0,
)
qr.add_data(jsonData)
qr.make(fit=True)
img = qr.make_image()

with open('QRtest.png','wb') as f:
    img.save(f)