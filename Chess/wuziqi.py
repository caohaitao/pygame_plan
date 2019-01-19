__author__ = 'ck_ch'
# -*- coding: utf-8 -*-
#!/usr/bin/env python
import numpy as np
import cv2
import threading
import time
import math

one_bar_length = 30
cross_nums = 15
dlg_width = (cross_nums+1)*one_bar_length
dlg_height = (cross_nums+1)*one_bar_length


class person:
    def __init__(self,value):
        self.poss = []
        self.value = value

    def is_win(self):
        for p in self.poss:
            x = p[0]
            y = p[1]



class Board:
    def __init__(self):
        self.width = (cross_nums-1)*one_bar_length
        self.height = (cross_nums-1)*one_bar_length
        self.persons = [person(0),person(1)]
        self.gap = 0
        self.who = 0

    def Draw(self,img):
        self.gap = int((dlg_width - self.width)/2)
        gap = self.gap
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(img,(gap,gap),(self.width+gap,self.height+gap),(0,0,0),thickness=1)
        for i in range(cross_nums-2):
            index = i+1
            cv2.line(img, (gap+index*one_bar_length, gap),
                     (gap+index*one_bar_length, gap+(cross_nums-1)*one_bar_length),
                     (0, 0, 0), 1)

            cv2.line(img, (gap, gap+index*one_bar_length),
                     (gap+(cross_nums-1)*one_bar_length, gap + index * one_bar_length),
                     (0, 0, 0), 1)

        for i in range(cross_nums):
            str = format("%d"%i)
            cv2.putText(img, str,
                        (gap+i*one_bar_length-int(one_bar_length/10), int(gap/2)),
                        font, one_bar_length/90, (0, 0, 0), 1)
            cv2.putText(img, str,
                        (int(gap/4),gap+i*one_bar_length),
                        font, one_bar_length/90, (0, 0, 0), 1)

        for p in self.persons:
            for pos in p.poss:
                pos_x = int(gap + pos[0]*one_bar_length)
                pos_y = int(gap + pos[1]*one_bar_length)
                c = p.value*255
                cv2.circle(img, (pos_x, pos_y), int(one_bar_length/4), (c,c,c), -1)

    def lbtn_down(self,x,y):
        ls = [x,y]

        indexs = [0,0]
        for i in range(len(ls)):
            v = ls[i]
            v = v - self.gap
            tx = int(v/one_bar_length)
            tx1 = int(tx+1)
            sub1 = math.fabs(v - tx*one_bar_length)
            sub2 = math.fabs(v - tx1*one_bar_length)
            if sub1<sub2:
                indexs[i] = tx
            else:
                indexs[i] = tx1

        p = self.persons[self.who]
        p.poss.append(indexs)
        self.who = int(1-self.who)

    def is_over(self):


class GamePlan:
    def __init__(self):
        self.board = Board()

    def Draw(self,img):
        self.board.Draw(img)

    def lbtn_down(self,x,y):
        self.board.lbtn_down(x,y)

def mouse_click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        gp.lbtn_down(x,y)


gp = GamePlan()
cv2.namedWindow('image')
cv2.setMouseCallback('image',mouse_click)
while True:
    c = np.array([96,164,200], np.uint8)
    img = np.ones((dlg_width, dlg_height,3), np.uint8)*c
    gp.Draw(img)
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break