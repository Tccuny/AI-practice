import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget, QLabel, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from hyperlpr import pipline as pp
import cv2
import os
import matplotlib
import json
import time
import jsonlines
import torch

def initJson():
    '''本小区车辆列表'''
    plates = [ "\u8d63BG6493", "\u7696AUB816", "\u6d59A222JH", "\u9c81L88888", "\u9c81LD9016", "\u4e91G55555","\u5409AA266G"]
    with open("localcars.json", "w") as f:
        for plate in plates:
            f.write(json.dumps({'plate': plate}))
            f.write('\n')
    with open("cheku.json", "w") as f:
        f.write(json.dumps({'total': 5, 'smallCars': 0, 'bigCars': 0}))
    with open("data.json", "w") as f:
        f.write("")

def carIsLocal(platea):
    with open("localcars.json", 'r') as f:
        cars_json = jsonlines.Reader(f)
        for car in cars_json:
            if car['plate'] == platea:
                return True
    return False
class Car(object):
    def __init__(self, plate, type, stime):
        self.plate = plate
        self.type = type
        self.stime = stime
    def obj_json(self, obj_instance):
        #print(type(obj_instance))
        return{
            'plate':obj_instance.plate,
            'type':obj_instance.type,
            'stime':obj_instance.stime
        }

def jsonToClass(car):
    return Car(car['plate'], car['type'], car['stime'])

class CarMesDb(object):
    __filename = ""
    def __init__(self, fileName):
        self.__filename = fileName
    def addCar(self, car):
        with open(self.__filename, 'a') as f:
            f.write(json.dumps(car, default=car.obj_json))
            f.write('\n')
    def getCarSTime(self, platea):
        with open(self.__filename, "r") as f:
            cars_json = jsonlines.Reader(f)
            for car in cars_json:
                if car['plate'] == platea:
                    return car['stime']
    def delCar(self, platea):
        plate = platea
        set = []
        with open(self.__filename, "r") as f:
            cars_json = jsonlines.Reader(f)
            for car in cars_json:
                #print(type(car))
                #print(car)
                #print(car['plate'])
                if car['plate'] != plate:
                    set.append(car)
        with open(self.__filename, 'w') as f:
            for car in set:
                f.write(json.dumps(car))
                f.write('\n')
    def isExist(self, platea):
        with open(self.__filename, "r") as f:
            cars_json = jsonlines.Reader(f)
            for car in cars_json:
                if car['plate'] == platea:
                    return True
        return False

class Example(QMainWindow):
    __fileName = "icons/title_icon.png"
    __chekuMesFile = "cheku.json"
    __localCars = "localcars.json"
    __image = ""
    __res = ""
    __tmpdir = "tmp"
    __plate_type = 0
    __carMesDb = CarMesDb("data.json")
    def __init__(self):
        super().__init__()
        self.initUI()

        isExists = os.path.exists(self.__tmpdir)
        if not isExists:
            os.makedirs(self.__tmpdir)

    def initUI(self):
        '''
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit applic0ation')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        '''
        #self.graphInit()
        #self.setGeometry(300, 300, 1000, 1000)

        #self.showMaximized();
        self.resize(1000,700)
        self.center()
        self.setWindowTitle('小区车辆信息管理系统')
        self.setWindowIcon(QIcon('icons/title_icon2.jpg'))
        self.graphInit()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def graphInit(self):
        self.statusBar().setStyleSheet("font-size:20px;font-family:楷体;background-color:black;color:white");
        self.statusBar().showMessage('欢迎使用本系统!')
        self.addLabel01()
        self.addSection02()
        self.addSection03()
        self.addSection04()
        pass

    def addLabel01(self):
        pixmap = QPixmap(self.__fileName)
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)
        self.lbl.setScaledContents(True)
        self.lbl.setGeometry(0,0,700,500)

    def addSection02(self):
        self.btn_in = QPushButton(self)
        self.btn_out = QPushButton(self)
        self.lbl2 = QLabel(self)
        self.lbl3 = QLabel(self)
        self.lbl4 = QLabel(self)
        self.lbl5 = QLabel(self)
        self.lbl6 = QLabel(self)
        self.lbl7 = QLabel(self)




        self.btn_in.setText("车辆入库")
        self.btn_out.setText("车辆出库")
        self.lbl2.setText("图片所在路径：")
        self.lbl2.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Arial;}")
        self.lbl3.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Arial;background-color:white;}")
        self.lbl3.setWordWrap(True)
        self.lbl4.setText("车牌位置识别：")
        self.lbl4.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Arial;}")
        self.lbl5.setScaledContents(True)
        self.lbl5.setStyleSheet("background-color:white;")
        self.lbl6.setText("车牌号码识别：")
        self.lbl6.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Arial;}")
        self.lbl7.setStyleSheet("QLabel{font-size:20px;font-weight:normal;font-family:楷体;background-color:white;}")

        self.btn_in.setGeometry(730, 10, 100, 30)
        self.btn_out.setGeometry(850, 10, 100, 30)
        self.lbl2.setGeometry(730, 50, 300, 30)
        self.lbl3.setGeometry(730, 90, 300, 60)
        self.lbl4.setGeometry(730, 200, 100, 30)
        self.lbl5.setGeometry(730, 250, 300, 100)
        self.lbl6.setGeometry(730, 370, 100, 30)
        self.lbl7.setGeometry(740, 410, 100, 30)

        self.btn_in.clicked.connect(lambda : self.showDialog('in'))
        self.btn_out.clicked.connect(lambda : self.showDialog('out'))

    def addSection03(self):
        self.lbl31 = QLabel(self)#标题
        self.lbl32 = QLabel(self)#车牌类型
        self.lbl33 = QLabel(self)#车辆类型
        self.lbl34 = QLabel(self) #省份

        self.lbl35 = QLabel(self)#是否本小区车辆
        self.lbl36 = QLabel(self)#是否有空位
        self.lbl37 = QLabel(self)#是否通过
        self.lbl38 = QLabel(self)  # 造访时间
        self.lbl39 = QLabel(self)  # 离开时间
        self.lbl310 = QLabel(self)  # 停车时长

        self.lbl302 = QLabel(self)
        self.lbl303 = QLabel(self)
        self.lbl304 = QLabel(self)
        self.lbl305 = QLabel(self)
        self.lbl306 = QLabel(self)
        self.lbl307 = QLabel(self)

        self.lbl35.setVisible(False)
        self.lbl36.setVisible(False)
        self.lbl37.setVisible(False)

        self.lbl38.setVisible(False)
        self.lbl39.setVisible(False)
        self.lbl310.setVisible(False)

        self.lbl31.setText("车辆信息识别")
        self.lbl31.setAlignment(Qt.AlignCenter)
        self.lbl32.setText("车牌类型：")
        self.lbl33.setText("车辆类型：")
        self.lbl34.setText("省份：")
        self.lbl35.setText("是否本小区车辆：")
        self.lbl36.setText("车库是否有空位：")
        self.lbl37.setText("是否允许进入：")
        self.lbl38.setText("造访时间：")
        self.lbl39.setText("离开时间：")
        self.lbl310.setText("停车时长/收费：")

        self.lbl31.setGeometry(0, 500, 700, 30)
        self.lbl32.setGeometry(0, 540, 100, 30)
        self.lbl33.setGeometry(350, 540, 100, 30)
        self.lbl34.setGeometry(0, 580, 100, 30)
        self.lbl35.setGeometry(350, 580, 100, 30)
        self.lbl36.setGeometry(0, 620, 100, 30)
        self.lbl37.setGeometry(350, 620, 150, 30)
        self.lbl38.setGeometry(350, 580, 100, 30)
        self.lbl39.setGeometry(0, 620, 100, 30)
        self.lbl310.setGeometry(350, 620, 150, 30)

        self.lbl302.setGeometry(110, 540, 100, 30)
        self.lbl303.setGeometry(460, 540, 300, 30)
        self.lbl304.setGeometry(110, 580, 100, 30)
        self.lbl305.setGeometry(460, 580, 200, 30)
        self.lbl306.setGeometry(110, 620, 200, 30)
        self.lbl307.setGeometry(460, 620, 200, 30)

        self.lbl302.setStyleSheet("font-family:楷体;font-size:20px")
        self.lbl303.setStyleSheet("font-family:楷体;font-size:20px")
        self.lbl304.setStyleSheet("font-family:楷体;font-size:20px")
        self.lbl305.setStyleSheet("font-family:楷体;font-size:20px")
        self.lbl306.setStyleSheet("font-family:楷体;font-size:20px")
        self.lbl307.setStyleSheet("font-family:楷体;font-size:20px")

        self.lbl31.setStyleSheet("background-color:white;font-family:楷体;font-size:20px")
        self.lbl37.setStyleSheet("font-size:15px;font-weight:bold")

        pass

    def addSection04(self):
        self.lbl41 = QLabel(self)
        self.lbl42 = QLabel(self)
        self.lbl43 = QLabel(self)
        self.lbl44 = QLabel(self)
        self.lbl402 = QLabel(self)
        self.lbl403 = QLabel(self)
        self.lbl404 = QLabel(self)

        self.lbl41.setGeometry(700, 500, 300, 30)
        self.lbl42.setGeometry(700, 540, 100, 30)
        self.lbl402.setGeometry(810, 540, 300, 30)
        self.lbl43.setGeometry(700, 580, 100, 30)
        self.lbl403.setGeometry(810, 580, 300, 30)
        self.lbl44.setGeometry(700, 620, 100, 30)
        self.lbl404.setGeometry(810, 620, 300, 30)

        self.lbl41.setStyleSheet("background-color:blue;font-family:楷体;font-size:20px;color:white")

        self.lbl41.setText("临时车辆车库信息")
        self.lbl41.setAlignment(Qt.AlignCenter)
        self.lbl42.setText("车库剩余停车位：")
        self.lbl43.setText("小型车辆：")
        self.lbl44.setText("大型车辆：")

        self.lbl402.setStyleSheet("background-color:white;")
        self.lbl403.setStyleSheet("background-color:white;")
        self.lbl404.setStyleSheet("background-color:white;")

        with open(self.__chekuMesFile, "r") as f:
            chekuMes = json.load(f)
            total = chekuMes['total']
            smallCars = chekuMes['smallCars']
            bigCars = chekuMes['bigCars']
            self.lbl402.setText(str(total-smallCars-bigCars))
            self.lbl403.setText(str(smallCars))
            self.lbl404.setText(str(bigCars))

    def showDialog(self, state):
        fname = QFileDialog.getOpenFileName(self, 'open file', 'img/')
        if fname[0]:
            try:
                self.__fileName = fname[0]
                self.lbl.setPixmap(QPixmap(self.__fileName))
                self.lbl3.setText(self.__fileName)
                self.lbl5.setPixmap(QPixmap(self.__fileName))
                img = cv2.imread(self.__fileName)
                b, g, r = cv2.split(img)
                img_rgb = cv2.merge([r, g, b])
                images = pp.detect.detectPlateRough(
                    img,  img.shape[0], top_bottom_padding_rate=0.1)
                platea = ""
                typea = ""
                stimea = 0.0
                for j, plate in enumerate(images):
                    plate, rect, origin_plate = plate
                    #print(rect)
                    plate_tmp = cv2.resize(plate, (136, 36 * 2))
                    self.__plate_type = pp.td.SimplePredict(plate_tmp)
                    tmpImg = img_rgb[int(rect[1]):int(
                        rect[1] + rect[3]), int(rect[0]):int(rect[0] + rect[2])]
                    matplotlib.image.imsave(self.__tmpdir + '/source.png', img_rgb)
                    matplotlib.image.imsave(self.__tmpdir+'/middle_res.png', tmpImg)
                    self.lbl5.setPixmap(QPixmap(self.__tmpdir+'/middle_res.png'))
                    image, res = pp.SimpleRecognizePlate(img)
                    os.system("cut.py")
                    #print(res)
                    self.__res = res[0]
                    platea = res[0]
                    self.lbl7.setText(res[0])
                if self.__plate_type == 0:
                    self.lbl302.setText("蓝底白字")
                    self.lbl303.setText('普通小型车')
                    typea = "普通小型车"
                else:
                    self.lbl302.setText("黄牌黑字")
                    self.lbl303.setText('大型车辆')
                    typea = "大型车辆"
                self.lbl304.setText(self.__res[0])
                self.lbl305.clear()
                self.lbl306.clear()
                self.lbl307.clear()
                total = 0
                smallCars = 0
                bigCars = 0
                with open(self.__chekuMesFile, "r") as f:
                    chekuMes = json.load(f)
                    total = chekuMes['total']
                    smallCars = chekuMes['smallCars']
                    bigCars = chekuMes['bigCars']
                if state == 'in':
                    self.statusBar().showMessage('车辆入库')
                    self.lbl35.setVisible(True)
                    self.lbl36.setVisible(True)
                    self.lbl37.setVisible(True)
                    self.lbl38.setVisible(False)
                    self.lbl39.setVisible(False)
                    self.lbl310.setVisible(False)
                    car = Car(platea, typea, time.time())
                    if self.__carMesDb.isExist(platea) == False:
                        self.__carMesDb.addCar(car)
                        if carIsLocal(platea):
                            self.lbl305.setText("是")
                            if total > smallCars + bigCars:
                                self.lbl306.setText("是")
                            else:
                                self.lbl306.setText("否")
                            self.lbl307.setText("是")
                            QMessageBox.information(self,
                                                    "通知",
                                                    "通知：本小区车辆'"+self.__res+"'入库成功！",
                                                    QMessageBox.Yes)
                        elif total > smallCars + bigCars:
                            if typea == "普通小型车":
                                smallCars = smallCars + 1
                            elif typea == "大型车辆":
                                bigCars = bigCars + 1
                            with open(self.__chekuMesFile, "w") as f:
                                json.dump({'total':total, 'smallCars': smallCars, 'bigCars': bigCars}, f)
                                self.lbl402.setText(str(total - smallCars - bigCars))
                                self.lbl403.setText(str(smallCars))
                                self.lbl404.setText(str(bigCars))
                                self.lbl305.setText("否")
                                self.lbl306.setText("是")
                                self.lbl307.setText("是")
                            QMessageBox.information(self,
                                                    "通知",
                                                    "通知：外来车辆'"+self.__res+"'入库成功！",
                                                    QMessageBox.Yes)
                        else:
                            self.lbl305.setText("否")
                            self.lbl306.setText("否")
                            self.lbl307.setText("否")
                            QMessageBox.warning(self,
                                                "警告",
                                                "通知：临时车库已满，外来车辆无法入内！",
                                                QMessageBox.Yes)
                    else:
                        QMessageBox.warning(self,
                                            "警告",
                                            "发生错误：该车辆已入库！",
                                            QMessageBox.Yes)
                else:
                    self.statusBar().showMessage('车辆出库')
                    self.lbl35.setVisible(False)
                    self.lbl36.setVisible(False)
                    self.lbl37.setVisible(False)
                    self.lbl38.setVisible(True)
                    self.lbl39.setVisible(True)
                    self.lbl310.setVisible(True)
                    if self.__carMesDb.isExist(platea) == True:
                        sTime = self.__carMesDb.getCarSTime(platea)
                        #print(sTime)
                        eTime = time.time()
                        self.lbl305.setText(time.asctime(time.localtime(sTime)))
                        self.lbl306.setText(time.asctime(time.localtime(eTime)))
                        cTime = int(eTime-sTime)
                        if carIsLocal(platea) == False:
                            self.lbl307.setText("%d小时%d分%d秒/%dRMB"%(cTime/3600, (cTime%3600)/60, cTime%60, int(cTime/3600+1)*50))
                        else:
                            self.lbl307.setText("%d小时%d分%d秒/不计费" % (cTime / 3600, (cTime % 3600) / 60, cTime % 60))
                        self.__carMesDb.delCar(platea)
                        if carIsLocal(platea) == False:
                            if typea == "普通小型车":
                                smallCars = smallCars - 1
                            elif typea == "大型车辆":
                                bigCars = bigCars - 1
                            with open(self.__chekuMesFile, "w") as f:
                                json.dump({'total': total, 'smallCars': smallCars, 'bigCars': bigCars}, f)
                                self.lbl402.setText(str(total - smallCars - bigCars))
                                self.lbl403.setText(str(smallCars))
                                self.lbl404.setText(str(bigCars))
                            QMessageBox.information(self,
                                                    "通知",
                                                    "通知：该外来车辆'"+self.__res+"'出库成功，停车计费"+str(int(cTime/3600+1)*50)+"RMB!",
                                                     QMessageBox.Yes)
                        else:
                            QMessageBox.information(self,
                                                    "通知",
                                                    "通知：该本小区车辆'"+self.__res+"'出库成功！",
                                                    QMessageBox.Yes)
                    else:
                        QMessageBox.warning(self,
                                            "警告",
                                            "发生错误：该车辆未曾入库！",
                                            QMessageBox.Yes)
                    #print(sTime)
            except:
                self.textEdit.setText("打开文件失败，可能是文件内型错误")

if __name__ == '__main__':
    initJson()
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())