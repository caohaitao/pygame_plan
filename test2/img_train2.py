__author__ = 'ck_ch'
# -*- coding: utf-8 -*-
import os
# third-party library
import torch
import torch.nn as nn
import cv2
import numpy as np
import os
import sys
from img_data_read2 import *

GPUID = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = GPUID

EPOCH = 800              # train the training data n times, to save time, we just train 1 epoch
BATCH_SIZE = 50
LR = 0.001              # 学习率

pkl_name = "rect_color3.pkl"

class CNN(nn.Module):
    def __init__(self,width,height):
        super(CNN, self).__init__()
        self.out = nn.Linear(width*height, 1)   # fully connected layer, output 10 classes

    def forward(self, x):
        x = x.view(x.size(0),-1)
        output = self.out(x)
        return output    # return x for visualization

cnn = CNN(2,2)
ndata = np.random.rand(2,4).astype(np.float32)
tdata = torch.from_numpy(ndata)
out = cnn(tdata)
print(out)