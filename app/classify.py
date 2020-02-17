import time
import datetime
from io import BytesIO
from PIL import Image, ImageFilter
import requests
import subprocess


def create_name_dic():
    name_dic = {}
    with open("../machikaneko_name.tsv") as f:
        for line in f.readlines():
            id_, name = line.rstrip().split('\t')
            name_dic[int(id_)] = name
    return name_dic


def detect_cat():
    now = datetime.datetime.now()
    now = int(time.mktime(now.timetuple()))

    image_paths = {}
    # 初期化
    print(subprocess.call("rm ../cat_detection/output/*tmp.png", shell=True))

    # ネコ検出
    print(subprocess.call("source venv/bin/activate; cd ../cat_detection; python pipeline.py ../app/tmp/tmp.png", shell=True))

    try:
        result_image = Image.open("../cat_detection/output/tmp.png")
        print(result_image.format, result_image.size, result_image.mode)
        image_paths["detect"] = f'static/images/detect_result_{now}.png'
        result_image.save(image_paths["detect"])
        bb_image = Image.open("../cat_detection/output/tmp-0-tmp.png")
        image_paths["bb"] = f'static/images/bb_result_{now}.png'
        bb_image.save(image_paths["bb"])
        resized_image = Image.open("../cat_detection/output/resized-tmp-0-tmp.png")
        image_paths["resize"] = f'static/images/resized_result_{now}.png'
        resized_image.save(image_paths["resize"])
    except:
        # 検出失敗
        return image_paths
    # 検出成功
    return image_paths


def classify(url):
    print(url)
    im = Image.open(BytesIO(requests.get(url).content))
    print(im.format, im.size, im.mode)
    im.save('tmp/tmp.png')

    res = []
    name_dic = create_name_dic()
    detected = detect_cat()
    if len(detected.items()) > 0:
        print(subprocess.call("source venv/bin/activate; cd ../classify; python predict_single_image.py ../app/static/images/resized_result.png", shell=True))
        with open("../classify/predict_single_result.tsv") as f:
            lines = f.readlines()
            for l in lines:
                class_, prob =  l.rstrip().split()
                class_ = int(class_)
                res.append({"class": class_, "name": name_dic[class_], "probability": prob})

    return detected, res

if __name__ == '__main__':
    pass
