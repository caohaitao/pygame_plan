__author__ = 'ck_ch'
import os
import cv2
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torchvision
import random

def read_one_data2(file_path):
    image = Image.open(file_path)
    image = np.array(image,dtype=np.float32)
    img = torch.from_numpy(image)
    w = image.shape[0]
    h = image.shape[1]
    c = image.shape[2]
    img = img.view(w,h,c)
    img = img.transpose(0,1).transpose(0,2).contiguous()
    return img,w,h

def read_datas2(dir):
    mps = {}
    for (root, dirs, files) in os.walk(dir):
        for item in files:
            spls = item.split('_')
            if len(spls) !=3:
                continue
            index = int(spls[1])
            mps[index] = item

    mpskeys = sorted(mps.keys())
    fs = []
    count = 0
    for k in mpskeys:
        fs.append(mps[k])
        count+=1
        if count == 20:
            break

    if count == 0:
        print("count is zero")

    w = 80
    h = 80
    label = np.ndarray(shape=len(fs),dtype='int64')
    res = np.ndarray(shape=(count, 3, w, h), dtype='float32')

    i=0
    for item in fs:
       file_path = format("%s\%s"%(dir,item))
       r, w, h = read_one_data2(file_path)
       res[i] = r
       l = file_path.replace('.bmp', '')
       ls = l.split('_')
       if len(ls) != 3:
           continue
       label[i] = GetRightLabel(int(ls[2]))
       i = i + 1
    return res,label,w,h


if __name__ == "__main__":
    #read_datas()
    #read_one_data2()
    res,label,w,h = read_datas2(r"imgs")