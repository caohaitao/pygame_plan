import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QThread
import numpy as np

dlg_width = 600
dlg_heigth = 600

def GetLocGPSFromFile(file_path):
    res = []
    for line in open(file_path):
        if line.find('loc:') != -1:
            splits = line.split('(')
            if len(splits) == 0:
                continue
            gps_str = splits[len(splits)-1]
            splits2 = gps_str.split(')')
            if len(splits2) == 0:
                continue
            gps_str = splits2[0]
            splits3 = gps_str.split(',')
            if len(splits3) != 2:
                continue
            lat = splits3[1]
            lon = splits3[0]
            lat = lat.strip(' ')
            lon = lon.strip(' ')
            write_str = lat+','+lon +','+'\r'

            flat = float(lat)
            flon = float(lon)
            if flat<0.1 or flon<0.1:
                continue
            res.append([flat,flon])
    nres = np.array(res)
    return nres

def trans_gps_to_rect(gps,rect_w,rect_h):
    scale = 100000
    max_lat = np.max(gps[:,0])
    min_lat = np.min(gps[:,0])
    max_lon = np.max(gps[:,1])
    min_lon = np.min(gps[:,1])
    gps[:,0] = (gps[:,0] - min_lat)*scale
    gps[:,1] = (gps[:,1] - min_lon)*scale
    lat_range = (max_lat-min_lat)*scale
    lon_range = (max_lon-min_lon)*scale
    lat_scale = lat_range/rect_w
    lon_scale = lon_range/rect_h
    gps[:, 0] = gps[:,0]/lat_scale
    gps[:, 1] = gps[:,1]/lon_scale
    return gps



class Example(QWidget):
    def __init__(self,gps):
        super().__init__()
        self.initUI()
        self.gps = gps
        self.count = 0
        t = QTimer(self)
        t.timeout.connect(self.update)
        t.start(200)

    def initUI(self):
        self.setGeometry(300, 300, dlg_width, dlg_heigth)
        self.setWindowTitle("Points")
        self.show()


    def paintEvent(self, e):
        qp =QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
        #qp.setPen(Qt.red)

        size = self.size()
        self.count += 1

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0,0,size.width(),size.height())
        qp.setBrush(QColor(100, 100, 100))

        temp_count=0
        for i in self.gps:
            x = int(i[0])
            y = int(i[1])
            qp.drawRect(x,y,1,1)
            temp_count += 1
            if temp_count==self.count:
                break

        qp.setBrush(QColor(255, 0, 0,200))
        x = int(gps[temp_count-1][0])
        y = int(gps[temp_count-1][1])
        qp.drawRect(x, y, 3, 3)

if __name__ == "__main__":
    gps = GetLocGPSFromFile(r"E:\work\OD\常州\00E0B453CA7F\trans_log\00E0B453CA7F4020.txt")
    gps = trans_gps_to_rect(gps,dlg_width,dlg_heigth)
    app = QApplication(sys.argv)
    ex = Example(gps)
    sys.exit(app.exec_())
