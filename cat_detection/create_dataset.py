import glob
import os
import random
import re
import subprocess

# 1匹だけ写っているネコの画像が110枚以上あるもののみ使う
# 100匹を学習、10匹をtestに使う
num_train_images = 100
num_test_images = 10


def create_image_list():
    image_dic = {}
    files = glob.glob('output/[0-9][0-9][0-9]-[0-9]-*.png')
    for f in files:
        _, catid, image_id, fileid = re.split('[-/]', f)
        image_dic[fileid] = image_dic.get(fileid, []) + [(catid, image_id)]
    return image_dic

def get_single_and_multiple_cat_images(image_dic):
    # 1匹のみまたは複数ネコを含んだ画像リストを作る
    single_images = {}
    multiple_images = []
    max_num_cat = 0
    max_fileid = 0
    for fileid, li in image_dic.items():
        if len(li) > 1:
            print(fileid + " has more than one cat.")
            multiple_images.append(fileid)
            if len(li) > max_num_cat:
                max_fileid = fileid
                max_num_cat = len(li)
        else:
            for catid, image_id in li:
                single_images[catid] = single_images.get(catid, []) + [fileid]
    print(len(multiple_images))
    print(max_fileid, image_dic[max_fileid])
    return single_images, multiple_images

image_dic = create_image_list()
single_cat_images, multiple_cat_images = get_single_and_multiple_cat_images(image_dic)


#print(single_cat_images)

train_samples = {}
test_samples = {}

for catid, image in single_cat_images.items():
    if len(image) < num_train_images+num_test_images:
        continue
    random_sample = random.sample(image, num_train_images+num_test_images)
    train_samples[catid] = random_sample[:num_train_images]
    test_samples[catid] = random_sample[num_train_images:]

#print(test_samples)
#print(multiple_cat_images)

os.makedirs('output/train', exist_ok=True)
os.makedirs('output/test', exist_ok=True)

with open('train_images.csv', 'w') as f:
    f.write(f'ImageName,ImageLabel\n')
    for catid, fileids in train_samples.items():
        for fileid in fileids:
            f.write(f'{catid}-0-{fileid}, {int(catid)}\n')

with open('test_images.csv', 'w') as f:
    f.write(f'ImageName,ImageLabel\n')
    for catid, fileids in test_samples.items():
        for fileid in fileids:
            f.write(f'{catid}-0-{fileid}, {int(catid)}\n')

def resize_sample(data_type='train'):
    with open(f'{data_type}_images.csv') as f:
        lines = f.readlines()[1:]
        for line in lines:
            filename, _= line.rstrip().split(',')
            print('.', end="", flush=True)
            subprocess.run(f'python resize_image.py output/{filename} output/{data_type}/{filename} 224', shell=True)

resize_sample('train')
resize_sample('test')
