__author__ = 'ck_ch'
# -*- coding: utf-8 -*-
import os
# third-party library
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import sys
import LossShow

EPOCH = 1000              # train the training data n times, to save time, we just train 1 epoch
BATCH_SIZE = 50
LR = 0.001              # 学习率

pkl_name = "rect_color2.pkl"

is_draw = False

class CNN(nn.Module):
    def __init__(self,width,height):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(         # input shape (1, 160, 160)
            nn.Conv2d(
                in_channels=3,              # input height
                out_channels=8,            # n_filters
                kernel_size=3,              # filter size
                stride=1,                   # filter movement/step
                padding=1,                  # if want same width and length of this image after con2d, padding=(kernel_size-1)/2 if stride=1
            ),                              # output shape (16, 160, 160)
            nn.BatchNorm2d(8),
            nn.ReLU(),                      # activation
            nn.MaxPool2d(kernel_size=2),    # choose max value in 2x2 area, output shape (16, 80, 80)
        )
        self.conv2 = nn.Sequential(         # input shape (16, 80, 80)
            nn.Conv2d(8, 16, 3, 1, 1),     # output shape (32, 80, 80)
            nn.BatchNorm2d(16),
            nn.ReLU(),                      # activation
            nn.MaxPool2d(2),                # output shape (32, 40, 40)
        )

        self.conv3 = nn.Sequential(         # input shape (32, 40, 40)
            nn.Conv2d(16, 32, 3, 1, 1),     # output shape (64, 40, 40)
            nn.BatchNorm2d(32),
            nn.ReLU(),                      # activation
            nn.MaxPool2d(2),                # output shape (64, 20, 20)
        )

        self.conv4 = nn.Sequential(
            nn.Conv2d(32,64,3,1,1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        out_one = int(int(width)/pow(2,4))
        self.out = nn.Linear(64 * out_one * out_one, 3)   # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = x.view(x.size(0), -1)           # flatten the output of conv2 to (batch_size, 128 * 10 * 10)
        output = self.out(x)
        return output    # return x for visualization

def train_model():
    ls = LossShow.LossShow(1,["red"],["loss1"])
    ls.plt_init()

    datas,labels,width,height=read_datas2("data\\")
    torch_datas = torch.from_numpy(datas)
    torch_labels = torch.from_numpy(labels)
    if os.path.exists(pkl_name):
        cnn = torch.load(pkl_name)
    else:
        cnn = CNN(width,height)
    print(cnn)
    optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)   # optimize all cnn parameters
    loss_func = nn.CrossEntropyLoss()                       # the target label is not one-hotted
    loss_func2 = torch.nn.MSELoss()
    for epoch in range(EPOCH):
        output = cnn(torch_datas)
        loss = loss_func2(output,torch_labels)
        if loss<0.0005:
            break
        ls.show([loss.detach().numpy()])

        print('epoch=%d loss=%0.4f'%(epoch,loss))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    torch.save(cnn,pkl_name)

    ls.stop()

    return cnn

def get_max_index(row):
    max_value = -999999999.0
    res = 0
    i = 0
    for a in row:
        if a>max_value:
            max_value = a
            res = i
        i = i+1
    return res

def cnn_test(cnn):
    datas,labels,w,h=read_datas2("test\\")
    torch_datas = torch.from_numpy(datas)
    torch_labels = torch.from_numpy(labels)
    out_put = cnn(torch_datas)

    numpy_labels = torch_labels.detach().numpy()
    numpy_outs = out_put.detach().numpy()

    count = len(numpy_outs)
    for i in range(count):
        count2 = len(numpy_outs[i])
        for j in range(count2):
            print("%d %0.4f-%0.4f"%(j,numpy_labels[i][j],numpy_outs[i][j]))

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("please input param [train|test]")
        exit()

    if len(sys.argv) >2:
        if sys.argv[2] == "draw":
            is_draw = True


    if sys.argv[1]=="train":
        cnn = train_model()
    elif sys.argv[1]=="test":
        cnn = torch.load(pkl_name)

    cnn_test(cnn)