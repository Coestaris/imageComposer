import base64
from PIL import Image

class ImageInfo:
    def __init__(self, path, im_hash, w, h, avcolor):
        self.path = path
        self.hash = im_hash
        self.w = w
        self.h = h
        self.avColor = avcolor


def to_gray(color):
    return color[0] * 299/1000 + color[1] * 587/1000 + color[2] * 114/1000


def calc_hash(im):

    # 1. Resize
    resized = im.resize((8, 8))

    # 2. To gray
    for x in range(0, resized.width):
        for y in range(0, resized.height):
            value = to_gray(resized.getpixel((x, y)))
            resized.putpixel((x, y), (value, value, value))

    # 3. Average
    avcolor = calc_av_color(resized)

    # 4 - 5. To bw, getting image bits
    bits = []
    for x in range(0, resized.width):
        for y in range(0, resized.height):
            value = resized.getpixel((x, y))
            if value[0] > avcolor:
                bits.append(1)
            else:
                bits.append(0)

    # 6. Getting hash from bits
    bytes = [0 for x in range(0, len(bits) // 8)]
    for index, bit in enumerate(bits):
        bytes[index // 8] = bytes[index // 8] | (bit << index % 8)

    return base64.b64encode(bytes)


def calc_av_color(im):
    avcolor = 0, 0, 0
    for x in range(0, im.width):
        for y in range(0, im.height):
            pixel = im.getpixel((x, y))
            avcolor[0] += pixel[0]
            avcolor[1] += pixel[1]
            avcolor[2] += pixel[2]

    pixelcount = im.width * im.height
    avcolor[0] /= pixelcount
    avcolor[1] /= pixelcount
    avcolor[2] /= pixelcount
    return avcolor


def get_img_info(path):
    img = Image.open(path)

    im_hash = calc_hash(img)
    avcolor = calc_av_color(img)

    info = ImageInfo(path, im_hash, img.width, img.height, avcolor)

    return info
