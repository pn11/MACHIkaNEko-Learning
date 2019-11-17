import torch
from cnn_finetune import make_model

import train

num_classes = 19

# モデル定義
model = make_model('vgg16', num_classes=num_classes, pretrained=True, input_size=(224, 224))

# パラメータの読み込み
param = torch.load('cnn_dict.model')

model.load_state_dict(param)

# 評価モードにする
model = model.eval()


test_set = train.MyDataSet('test_images.csv', '../cat_detection/output/test')

test_loader = torch.utils.data.DataLoader(test_set, batch_size=32)


from sklearn.metrics import classification_report

pred = []
Y = []
labels = [4, 7, 11, 18, 26,
          30, 34, 38, 42, 48,
          50, 55, 63, 66, 72,
          74, 81, 91, 96]

for i, (x,y) in enumerate(test_loader):
    with torch.no_grad():
        output = model(x)
    pred += [labels[int(l.argmax())] for l in output]
    Y += [labels[int(l)] for l in y]
    
print(classification_report(Y, pred))
