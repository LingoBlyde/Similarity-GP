import numpy

__author__ = 'Blyde'

from PIL import Image


def image_different(img_1, img_2, size=(512, 512)):
    if img_1.size != img_2.size:
        img_1 = img_1.resize(size, Image.ANTIALIAS)
        img_2 = img_2.resize(size, Image.ANTIALIAS)

    img_array_1 = numpy.array(img_1.getdata())
    img_array_2 = numpy.array(img_2.getdata())
    diff_num = 0
    for pixels_l, pixels_r in zip(img_array_1, img_array_2):
        if not _diff_pixel(pixels_l, pixels_r):
            diff_num += 1

    return float(diff_num) / (size[0] * size[1])


def _diff_pixel(pixels_l, pixels_r):
    try:
        for l, r in zip(pixels_l, pixels_r):
            if l != r:
                return False
        return True
    except:
        return False

if __name__ == '__main__':
    img_1 = Image.open('res/icon/left.png')
    img_2 = Image.open('res/icon/ight.png')
    print img_1.size
    print image_different(img_1, img_2)
