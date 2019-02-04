import base64
from array import array

from PIL import Image


class ImageInfo:
    def __init__(self, path, im_hash, w, h, avcolor, file_index):
        self.path = path
        self.im_hash = im_hash
        self.w = w
        self.h = h
        self.fileIndex = file_index
        self.avColor = avcolor

    def to_json(self):
        return {
            "path": self.path,
            "im_hash": self.im_hash,
            "w": self.w,
            "h": self.h,
            "avColor": self.avColor,
            "fileIndex": self.fileIndex
        }

def to_gray(color):
    return color[0] * 299/1000 + color[1] * 587/1000 + color[2] * 114/1000


def calc_hash(im):

    # 1. Resize
    resized = im.resize((8, 8))
    avcolor = 0

    # 2. To gray
    pixels = list(resized.getdata())
    for index, pixel in enumerate(pixels):
        pixels[index] = to_gray(pixel)
        avcolor += pixels[index]

    # 3. Average
    avcolor /= len(pixels)

    # 4 - 5. To bw, getting image bits
    bits = []
    for index, pixel in enumerate(pixels):
            if pixel > avcolor:
                bits.append(1)
            else:
                bits.append(0)

    # 6. Getting hash from bits
    bytes = [0 for x in range(0, len(bits) // 8)]
    for index, bit in enumerate(bits):
        bytes[index // 8] = bytes[index // 8] | (bit << index % 8)

    #string = "".join([chr(x) for x in bytes])
    data_bytes = array('B', bytes) #string.encode("utf-8")

    return base64.b64encode(data_bytes)


def calc_av_color(im):
    avcolor = [0, 0, 0]
    pixels = list(im.getdata())

    for pixel in pixels:
        r, g, b = pixel
        avcolor[0] += r
        avcolor[1] += g
        avcolor[2] += b

    pixelcount = im.width * im.height
    avcolor[0] /= pixelcount
    avcolor[1] /= pixelcount
    avcolor[2] /= pixelcount
    return avcolor


def hash_diff(hash1, hash2):
    decoded1 = base64.b64decode(hash1)
    decoded2 = base64.b64decode(hash2)

    diff = 0
    for index in range(1, len(decoded1)):
        diff += abs(decoded1[index] - decoded2[index])

    return [diff, diff / (8 * 256) * 100]


def get_img_info(path, index):
    img = Image.open(path)

    im_hash = str(calc_hash(img))

    avcolor = calc_av_color(img)

    info = ImageInfo(path, im_hash, img.width, img.height, avcolor, index)
    return info
