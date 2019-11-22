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
    # 初期化
    print(subprocess.call("rm ../cat_detection/*tmp.png", shell=True))
    print(subprocess.call("rm static/images/detect_result.png static/images/bb_result.png static/images/resized_result.png", shell=True))

    # ネコ検出
    print(subprocess.call("source venv/bin/activate; cd ../cat_detection; python pipeline.py ../app/tmp/tmp.png", shell=True))

    try:
        result_image = Image.open("../cat_detection/output/tmp.png")
        print(result_image.format, result_image.size, result_image.mode)
        result_image.save('static/images/detect_result.png')

        bb_image = Image.open("../cat_detection/output/tmp-0-tmp.png")
        bb_image.save('static/images/bb_result.png')
        resized_image = Image.open("../cat_detection/output/resized-tmp-0-tmp.png")
        resized_image.save('static/images/resized_result.png')
    except:
        # 検出失敗
        return False
    # 検出成功
    return True


def classify(url):
    print(url)
    im = Image.open(BytesIO(requests.get(url).content))
    print(im.format, im.size, im.mode)
    im.save('tmp/tmp.png')

    res = []
    name_dic = create_name_dic()
    if detect_cat():
        print(subprocess.call("source venv/bin/activate; cd ../classify; python predict_single_image.py ../app/static/images/resized_result.png", shell=True))
        with open("../classify/predict_single_result.tsv") as f:
            lines = f.readlines()
            for l in lines:
                class_, prob =  l.rstrip().split()
                class_ = int(class_)
                res.append({"class": class_, "name": name_dic[class_], "probability": prob})

    return res

if __name__ == '__main__':
    pass
