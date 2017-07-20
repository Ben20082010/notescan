from wand.image import Image
from wand.color import Color



im = Image(filename='test/template/note.pdf', resolution=300)
# im = Image(filename='test/M4/collision.pdf', resolution=300)

for i, page in enumerate(im.sequence):
    with Image(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='page-%s.jpg' % i)

