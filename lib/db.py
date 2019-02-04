import glob
import json
import os

from lib.img_processor import ImageInfo


def load(dirname):
    files = [y for x in os.walk(dirname) for y in glob.glob(os.path.join(x[0], '*.json'))]

    result = []
    for file in files:
        with open(file, "r") as f:
            object = json.load(f)
            result.append(ImageInfo(
                    path=object["path"],
                    im_hash=object["im_hash"],
                    w=object["w"],
                    h=object["h"],
                    avcolor=object["avColor"],
                    file_index=object["fileIndex"]
                )
            )

    return result