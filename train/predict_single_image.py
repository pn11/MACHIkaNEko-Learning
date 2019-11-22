from cnn_finetune import make_model
from PIL import Image
import sys
import torch
import torchvision.transforms as transforms

argv = sys.argv
if len(argv) != 2:
    exit()

# 画像読み込み
image = Image.open(argv[1])
image = image.convert('RGB') # PyTorch 0.4以降
transform = transforms.Compose([transforms.ToTensor()])
image = transform(image)
# Not yet understood but said in
# https://discuss.pytorch.org/t/runtimeerror-expected-4-dimensional-input-for-4-dimensional-weight-6-3-5-5-but-got-3-dimensional-input-of-size-3-256-256-instead/37189
image = image.unsqueeze(0)

num_classes = 19
# モデル定義
model = make_model('vgg16', num_classes=num_classes, pretrained=True, input_size=(224, 224))

# パラメータの読み込み
param = torch.load('cnn_dict.model', map_location=torch.device('cpu'))

model.load_state_dict(param)

# 評価モードにする
model = model.eval()

labels = [4, 7, 11, 18, 26,
          30, 34, 38, 42, 48,
          50, 55, 63, 66, 72,
          74, 81, 91, 96]

#outputs = net(inputs)
with torch.no_grad():
    output = model(image)
    softmax = torch.nn.Softmax()
    top4_prob, top4_label = torch.topk(output, 4)
    
    probs = softmax(output)

    for ind in top4_label[0].tolist():
        print(f"{labels[ind]}: {probs[0][ind]*100} %")

    with open("predict_single_result.tsv", "w") as fw:
        for ind in top4_label[0].tolist()[:3]:
            fw.write(f"{labels[ind]}\t{probs[0][ind]*100}%\n")
