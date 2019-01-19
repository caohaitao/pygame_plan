__author__ = 'ck_ch'
import os
import cv2
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torchvision
import random

def read_one_data(file_path):
    im = cv2.imread(file_path)
    w = im.shape[0]
    h = im.shape[1]
    data = (cv2.cvtColor(im,cv2.COLOR_BGR2RGB)/255.0).reshape(3,w,h).astype(np.float32)
    return data,w,h
    # cv2.imshow("image",gray)
    # cv2.waitKey(0)

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

def read_datas(dir):
    #dir = 'data\\'
    for (root,dirs,files) in os.walk(dir):
        print(len(files))
        #res = np.ndarray(shape=(len(files),1,width,height),dtype='float32')
        label = np.ndarray(shape=(len(files)),dtype='int64')
        label2 = np.ndarray(shape=(len(files),2),dtype='float32')
        i = 0
        for item in files:
            file_path = format("%s%s"%(dir,item))
            r,w,h = read_one_data2(file_path)
            if i==0:
                res = np.ndarray(shape=(len(files),3,w,h),dtype='float32')
            res[i]= r
            sl = item.replace('.jpg','')
            sls = sl.split('_')
            label[i] = int(sls[1])
            label2[i][0] = float(sls[2])
            label2[i][1] = float(sls[3])
            i = i+1
    return res,label,label2,w,h

def GetRightLabel(l,x):

    if x <40:
        return 2
    else:
        return 1

    if x > 65:
        return 1

    # while True:
    #     res = random.randint(0,2)
    #     if res != l:
    #         return res

# def read_datas2(dir):
#     for (root,dirs,files) in os.walk(dir):
#         print(len(files))
#         count = int(len(files))
#         label = np.ndarray(shape=(count),dtype='int64')
#         i = 0
#         for item in files:
#             if item.find('.bmp') == -1:
#                 continue
#             file_path = format("%s\%s"%(dir,item))
#             r,w,h = read_one_data2(file_path)
#             if i==0:
#                 res = np.ndarray(shape=(count,3,w,h),dtype='float32')
#             res[i] = r
#             l = file_path.replace('.bmp','')
#             ls = l.split('_')
#             if len(ls) != 3:
#                 continue
#             #label[i] = int(ls[2])
#             label[i] = GetRightLabel(int(ls[2]))
#             i = i + 1
#     return res,label,w,h

def read_datas2(dir):
    mps = {}
    for (root, dirs, files) in os.walk(dir):
        for item in files:
            spls = item.split('_')
            if len(spls) !=4:
                continue
            index = int(spls[1])
            mps[index] = item

    mpskeys = sorted(mps.keys())
    mpskeys.reverse()
    count = 0
    i = 0

    whole_nums = 0

    whole_nums = len(mpskeys)

    w = 80
    h = 80
    label = np.ndarray(shape=whole_nums,dtype='int64')
    res = np.ndarray(shape=(whole_nums, 3, w, h), dtype='float32')

    wrong_form = [0,0,0]
    wrong_index = []

    avg_pos_x = 0

    wrong_use_nums = 20

    for k in mpskeys:
        file_path = format("%s\%s"%(dir,mps[k]))
        r, w, h = read_one_data2(file_path)
        res[count] = r
        l = file_path.replace('.bmp', '')
        ls = l.split('_')
        if len(ls) != 4:
            continue
        if count<wrong_use_nums:
            wrong_form[int(ls[2])]+=1
            wrong_index.append(count)
            #label[count] = GetRightLabel(int(ls[2]))
            avg_pos_x += int(ls[3])
        else:
            label[count] = int(ls[2])
        count+=1
        if count==whole_nums:
            break

    avg_pos_x/=wrong_use_nums

    max_index = -1
    max_num = -1
    for i in range(3):
        if wrong_form[i]>max_num:
            max_num = wrong_form[i]
            max_index = i

    right_index = GetRightLabel(max_index,avg_pos_x)
    print("avg_pos",avg_pos_x,"right_index",right_index)
    for i in wrong_index:
        label[i] = right_index

    if count == 0:
        print("count is zero")

    return res,label,w,h


if __name__ == "__main__":
    #read_datas()
    #read_one_data2()
    res,label,w,h = read_datas2(r"imgs")
