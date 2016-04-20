import PIL
import numpy
from PIL import Image


def different(hash1, hash2):
    """ Compute hamming distance of two hash """
    if hash1 is None or hash2 is None:
        raise TypeError('Hash must not be None.')

    if hash1.size != hash2.size:
        raise TypeError('ImageHashes must be of the same shape.', hash1.shape, hash2.shape)

    return (hash1.flatten() != hash2.flatten()).sum()


def dhash(image_obj, hash_size=8):
    # For this implementation we create a 8x9 image.
    image_obj = image_obj.convert("L").resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image_obj.getdata(), dtype=numpy.float).reshape((hash_size + 1, hash_size))
    # compute differences
    diff = pixels[1:, :] > pixels[:-1, :]
    return diff

def phash(image_obj, hash_size=8):
    image_obj = image_obj.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image_obj.getdata(), dtype=numpy.float).reshape((hash_size, hash_size))
    dct = scipy.fftpack.dct(pixels)
	dctlowfreq = dct[: hash_size, 1: hash_size + 1]
	avg = dctlowfreq.mean()
	diff = dctlowfreq > avg
    return diff


if __name__ == '__main__':
    img1 = PIL.Image.open('res/1.png')
    img2 = PIL.Image.open('res/2.png')
    similarity = different(dhash(img1), dhash(img2))
    similarity = different(phash(img1), phash(img2))
    print similarity
