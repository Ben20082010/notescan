from wand.image import Image
from wand.color import Color



# im = Image(filename='template/note_alt.pdf', resolution=600)
im = Image(filename='template/note.pdf', resolution=600)

# im = Image(filename='destination.pdf', resolution=300)

for i, page in enumerate(im.sequence):
    with Image(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='cache/page-%s.jpg' % i)

