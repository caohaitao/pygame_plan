__author__ = 'ck_ch'
# -*- coding: utf-8 -*-
#!/usr/bin/env python

import threading
import time

import numpy as np
import cv2
import random
import os
import shutil
import copy

dlg_width = int(80)
dlg_heigth = int(80)
rect_length = int(12)
move_speed = int(2)

class TPos:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)

class TObject:
    def __init__(self,pos,color):
        self.pos = pos
        self.length = rect_length
        self.color = color

    def Draw(self,img):
        x0 = int(self.pos.x-rect_length/2)
        y0 = int(self.pos.y-rect_length/2)
        x1 = int(self.pos.x+rect_length/2)
        y1 = int(self.pos.y+rect_length/2)
        cv2.rectangle(img, (x0,y0), (x1,y1), self.color, thickness=-1)

    def MoveDown(self):
        self.pos = TPos(self.pos.x,self.pos.y+move_speed)
        if self.pos.y>dlg_heigth:
            return False
        return True
    def MoveLeft(self):
        if self.pos.x > rect_length/2:
            self.pos = TPos(self.pos.x-move_speed,self.pos.y)
            return True
        return False

    def MoveRight(self):
        if self.pos.x < (dlg_width - rect_length/2):
            self.pos = TPos(self.pos.x + move_speed, self.pos.y)
            return True
        return False

    def Cross(self,other):
        sub_x = abs(self.pos.x - other.pos.x)
        sub_y = abs(self.pos.y - other.pos.y)
        if sub_x<rect_length and sub_y<rect_length:
            print(self.pos,other.pos)
            return True
        return False

class GamePlan:
    def __init__(self):
        people_pos = TPos(dlg_width/2,dlg_heigth-rect_length/2)
        self.people = TObject(people_pos,(200,0,0))
        self.enemys = []
        self.last_enemy_product_time = 0
        self.score = 0

        self.t = threading.Timer(0.2,self.enimy_move)
        self.t.start()

        self.t2 = threading.Timer(0.2,self.auto_move)
        self.t2.start()
        self.is_over = False
        self.image = None
        self.save_count = 0
        self.draw_count = 0


    def Draw(self,img):
        self.people.Draw(img)
        for e in self.enemys:
            e.Draw(img)

        self.image = copy.copy(img)
        self.draw_count+=1

        font = cv2.FONT_HERSHEY_SIMPLEX
        str = format("score(%d)"%self.score)
        cv2.putText(img, str, (0,10), font, 0.4, (0,0,0), 1)

    def auto_move(self):
        r = random.randint(0,2)
        m = 0
        if r == 0:
            m = r
        elif r == 1:
            if self.people.MoveLeft() == True:
                m = r
            else:
                m = 0

        elif r == 2:
            if self.people.MoveRight() == True:
               m = r
            else:
                m = 0

        if self.draw_count>0:
            bmp_name = format("imgs\\img_%d_%d.bmp"%(self.save_count,m))
            cv2.imwrite(bmp_name, self.image)
            self.save_count += 1

        if self.is_over == False:
            self.t2 = threading.Timer(0.2,self.auto_move)
            self.t2.start()

    def quit(self):
        self.is_over = True

    def enimy_move(self):
        if len(self.enemys)<1:
            if (time.time()*1000 - self.last_enemy_product_time)>8000:
                self.ProductAEnemy()

        del_objs = []
        for e in self.enemys:
            if e.MoveDown() == False:
                del_objs.append(e)

            if self.people.Cross(e):
                print("cross")
                print("score=%d"%self.score)
                self.quit()

        for e in del_objs:
            self.enemys.remove(e)
            self.score += 1

        if self.is_over == False:
            self.t = threading.Timer(0.2,self.enimy_move)
            self.t.start()

    def ProductAEnemy(self):
        self.last_enemy_product_time = time.time()*1000
        rand_x = random.randint(rect_length/2,dlg_width-rect_length/2)
        y = rect_length/2
        enemy = TObject(TPos(rand_x,y),(0,200,0))
        self.enemys.append(enemy)

if os.path.exists("imgs\\"):
    shutil.rmtree("imgs\\")
os.mkdir("imgs")

gp = GamePlan()
while True:
    if gp.is_over == True:
        break
    img = np.ones((dlg_width,dlg_heigth,3), np.uint8)*255
    gp.Draw(img)
    cv2.imshow('image',img)
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break
