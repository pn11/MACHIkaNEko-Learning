from io import BytesIO
from PIL import Image, ImageFilter
import requests

name_dic = {
    "001": "ネコバス",
    "002": "???",
    "003": "???",
}

def classify(url):
    print(url)
    im = Image.open(BytesIO(requests.get(url).content))
    print(im.format, im.size, im.mode)

    # 1. detect cat
    # 2. trim and resize
    # 3. classify
    res = [
        {"class": "001",
         "name": name_dic["001"],
         "probability": 1.0
        },
        {"class": "002",
         "name": name_dic["002"],
         "probability": 1.0
        },
        {"class": "003",
         "name": name_dic["003"],
         "probability": 1.0
        }
    ]
    
    return res
