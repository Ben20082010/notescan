from wand.image import Image
from wand.color import Color



# im = Image(filename='i/note.pdf', resolution=600)
# im = Image(filename='test/M4/relative motion.pdf', resolution=600)
im = Image(filename='template/8:0', resolution=100)

# im = Image(filename='destination.pdf', resolution=300)


with Image(im.sequence[0]) as page_image:
    page_image.alpha_channel = True
    page_image.save(filename='cache/notex.jpg')


#
#
# for i, page in enumerate(im.sequence):
#     with Image(page) as page_image:
#         page_image.alpha_channel = False
#         page_image.save(filename='cache/page-%s.jpg' % i)
#
