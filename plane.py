import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen,QFont,QPixmap,QImage
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QThread
from PyQt5.QtCore import *
import numpy as np
import time
import os
import shutil

dlg_width = 200
dlg_heigth = 200
rect_length = 20
move_speed = 10

class TObject:
    def __init__(self,pos,color):
        self.pos = pos
        self.length = rect_length
        self.color = color

    def Draw(self,qp):
        qp.setBrush(self.color)
        qp.drawRect(self.pos.width()-rect_length/2,self.pos.height()-rect_length/2,rect_length,rect_length)

    def MoveDown(self):
        self.pos = QSize(self.pos.width(),self.pos.height()+move_speed)
        if self.pos.height()>dlg_heigth:
            return False
        return True
    def MoveLeft(self):
        if self.pos.width() > rect_length/2:
            self.pos = QSize(self.pos.width()-1,self.pos.height())
            return True
        return False

    def MoveRight(self):
        if self.pos.width() < (dlg_width - rect_length/2):
            self.pos = QSize(self.pos.width() + 1, self.pos.height())
            return True
        return False

    def Cross(self,other):
        sub_x = abs(self.pos.width() - other.pos.width())
        sub_y = abs(self.pos.height() - other.pos.height())
        if sub_x<rect_length and sub_y<rect_length:
            print(self.pos,other.pos)
            return True
        return False

class MainDlg(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        t = QTimer(self)
        t.timeout.connect(self.update)
        t.start(200)

        t2 = QTimer(self)
        t2.timeout.connect(self.enimy_move)
        t2.start(200)

        t3 = QTimer(self)
        t3.timeout.connect(self.auto_move)
        t3.start(100)

        people_pos = QSize(dlg_width/2,dlg_heigth-rect_length/2)
        self.people = TObject(people_pos,QColor(200,0,0))
        self.enemys = []
        self.last_enemy_product_time = 0
        self.score = 0
        self.is_save = False

        self.save_count = 0

        if os.path.exists("imgs\\"):
            shutil.rmtree("imgs\\")
        os.mkdir("imgs")

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

        bmp_name = format("imgs\\img_%d_%d.bmp"%(self.save_count,m))
        self.pixmap.save(bmp_name)
        self.save_count += 1

    def enimy_move(self):
        if len(self.enemys)<6:
            if (time.time() - self.last_enemy_product_time)>2:
                self.ProductAEnemy()

        del_objs = []
        for e in self.enemys:
            if e.MoveDown() == False:
                del_objs.append(e)

            if self.people.Cross(e):
                print("cross")
                exit()
        for e in del_objs:
            self.enemys.remove(e)
            self.score += 1

    def initUI(self):
        self.setGeometry(800, 700, dlg_width, dlg_heigth)
        self.setWindowTitle("Plane")
        self.show()

    def paintEvent(self, e):
        #pixmap = QImage(dlg_width, dlg_heigth)
        self.pixmap = QImage(dlg_width, dlg_heigth,QImage.Format_RGB888)
        qp = QPainter(self.pixmap)
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        qp = QPainter()

        qp.begin(self)
        self.drawMap(qp,self.pixmap)
        qp.end()

        if self.is_save:
            # for x in range(pixmap.width()):
            #     for y in range(pixmap.height()):
            #         r = pixmap.pixel(x,y)
            #         a = QColor(r).getRgb()
            #         print(a)
            self.pixmap.save("e:\\a.bmp")
            self.is_save = False

    def ProductAEnemy(self):
        self.last_enemy_product_time = time.time()
        rand_x = random.randint(rect_length/2,dlg_width-rect_length/2)
        y = rect_length/2
        enemy = TObject(QSize(rand_x,y),QColor(0,200,0))
        self.enemys.append(enemy)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.is_save = True
        elif e.key() == Qt.Key_Left:
            self.people.MoveLeft()
        elif e.key() == Qt.Key_Right:
            self.people.MoveRight()

    def drawMap(self,qp,map):
        #qp.drawPixmap(QPoint(0,0),map)
        qp.drawImage(0,0,map)

        qp.setPen(QColor(168,34,3))
        text_rect = QRect(2,2,60,30)
        qp.setFont(QFont("Decorative", 10))
        text = format("score(%d)"%self.score)
        qp.drawText(text_rect,Qt.AlignCenter,text)

    def drawPoints(self, qp):

        size = self.size()

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0,0,size.width(),size.height())

        self.people.Draw(qp)
        for e in self.enemys:
            e.Draw(qp)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainDlg()
    sys.exit(app.exec_())
