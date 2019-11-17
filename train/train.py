from cnn_finetune import make_model
import datetime
import os
import pandas as pd
from PIL import Image
import pretrainedmodels
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset
import torchvision.transforms as transforms

labels = [4, 7, 11, 18, 26,
          30, 34, 38, 42, 48,
          50, 55, 63, 66, 72,
          74, 81, 91, 96]
label_dic = {l:i for i, l in enumerate(labels)}
print(label_dic)
num_classes = len(labels)
model_name = 'vgg16'
batch_size = 32
learning_rate = 0.001

def prepare_model():
    # cnn_futureを使う場合
 #   model = make_model(model_name, num_classes=num_classes, pretrained=True, input_size=(224, 224))
    model = make_model(model_name, num_classes=num_classes, pretrained=False, input_size=(224, 224))
    # pretrainedmodelsを使う場合
#    model = pretrainedmodels.__dict__[model_name](num_classes=num_classes, pretrained='imagenet')
    # 'cuda' or 'cpu'
    device = torch.device('cuda')
    model = model.to(device)

    return model, device

class MyDataSet(Dataset):
    def __init__(self, csv_path, root_dir):
        self.train_df = pd.read_csv(csv_path)
        print(self.train_df)
        self.root_dir = root_dir
        self.images = os.listdir(self.root_dir)
        self.transform = transforms.Compose([transforms.ToTensor()])
    def __len__(self):
        return len(self.images)
        
    def __getitem__(self, idx):
        # 画像読み込み
        image_name = self.images[idx]
        image = Image.open( os.path.join(self.root_dir, image_name) )
        image = image.convert('RGB') # PyTorch 0.4以降
        # label 0, ..., 18
        label = self.train_df.query('ImageName=="'+image_name+'"')['ImageLabel'].iloc[0]
            
        return self.transform(image), label_dic[int(label)]


def prepare_dataset():
    train_set = MyDataSet('train_images.csv', '/home/oka/git/machikaneko-learning/cat_detection/output/train')
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)

    return train_loader


def train(epoch):  
    total_loss = 0
    total_size = 0
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        total_loss += loss.item()
        total_size += data.size(0)
        loss.backward()
        optimizer.step()
        if batch_idx % 1000 == 0:
            now = datetime.datetime.now()
            print('[{}] Train Epoch: {} [{}/{} ({:.0f}%)]\tAverage loss: {:.6f}'.format(
                                now,
                                epoch, batch_idx * len(data), len(train_loader.dataset),
                                100. * batch_idx / len(train_loader), total_loss / total_size))
            with open('train.log', 'a') as f:
                f.write(f'{epoch} {total_loss/total_size}\n')


if __name__ == '__main__':
    model, device = prepare_model()
    train_loader = prepare_dataset()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)
#    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    nepoch = 500
    for epoch in range(1, nepoch + 1):
        train(epoch)

    torch.save(model.state_dict(), 'cnn_dict.model')              
    torch.save(model, 'cnn.model')

    # Prediction

    model = make_model('vgg16', num_classes=num_classes, pretrained=True, input_size=(224, 224))
    # パラメータの読み込み
    param = torch.load('cnn_dict.model')

    model.load_state_dict(param)

    # 評価モードにする
    model = model.eval()

    test_set = MyDataSet('test_images.csv', '../cat_detection/output/test')
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=32)


    from sklearn.metrics import classification_report

    pred = []
    Y = []
    for i, (x,y) in enumerate(test_loader):
        with torch.no_grad():
            output = model(x)
        pred += [labels[int(l.argmax())] for l in output]
        Y += [labels[int(l)] for l in y]

    print(classification_report(Y, pred))
