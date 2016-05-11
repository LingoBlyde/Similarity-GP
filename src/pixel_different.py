import numpy

__author__ = 'Blyde'

from PIL import Image


def pixel_different(img_1, img_2, gray=False, threshold=0):
    if img_1.size != img_2.size:
        img_2 = img_2.resize(img_1.size, Image.ANTIALIAS)

    if gray:
        img_1, img_2 = img_1.convert("L"), img_2.convert("L")

    img_array_1 = numpy.array(img_1.getdata())
    img_array_2 = numpy.array(img_2.getdata())
    diff_num = 0
    for pixels_l, pixels_r in zip(img_array_1, img_array_2):
        if not _is_same_pixel(pixels_l, pixels_r, threshold):
            diff_num += 1

    return float(diff_num) / (img_1.size[0] * img_1.size[1])


def _is_same_pixel(pixels_l, pixels_r, threshold=0):
    if isinstance(pixels_l, numpy.ndarray) and isinstance(pixels_r, numpy.ndarray) and len(pixels_r) == len(pixels_l):
        for l, r in zip(pixels_l, pixels_r):
            if l != r:
                return False
    else:
        if abs(pixels_l - pixels_r) > threshold:
            return False
    return True


if __name__ == '__main__':
    img1 = Image.open('res/icon/left.png')
    img2 = Image.open('res/icon/ight.png')
    print pixel_different(img1, img2, gray=True, threshold=0)
