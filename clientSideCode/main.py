import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets                     # uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, 
                             QLabel, QVBoxLayout, QMessageBox)              # +++

from test2_ui import Ui_Form                                   # +++
import requests
import encryptor
import RPi.GPIO as g
import csv, time
import json
class video (QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()                  
        self.toggle = True
#        uic.loadUi('test2.ui',self)                           # ---
        self.setupUi(self)     
        #you need to set the customizeWindowHint first and then closeButtonhint will work
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)          
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)                     
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        self.capture.clicked.connect(self.capture_image)
        # self.capture.clicked.connect(self.startUIWindow)       # - ()
        self.image_label.setScaledContents(True)
        self.cap = None                                        #  -capture <-> +cap
        self.timer = QtCore.QTimer(self, interval=5)
        self.timer.timeout.connect(self.update_frame)
        self._image_counter = 0
        #launches the webcam
        self.start_webcam()


    def keyPressEvent(self,e):
        if e.modifiers() & QtCore.Qt.ShiftModifier and e.modifiers() & QtCore.Qt.ControlModifier:
            if self.toggle:
                self.setWindowFlags(
                    QtCore.Qt.CustomizeWindowHint |
                    QtCore.Qt.WindowCloseButtonHint |
                    QtCore.Qt.WindowStaysOnTopHint|
                    QtCore.Qt.WindowMaximizeButtonHint|QtCore.Qt.WindowMinimizeButtonHint
                    )
                self.toggle = not self.toggle 
                self.show()
    def closeEvent(self,e):
        if self.toggle:
            e.ignore()
    @QtCore.pyqtSlot()
    def start_webcam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.timer.start()

    @QtCore.pyqtSlot()
    def update_frame(self):
        ret, image = self.cap.read()
        simage     = cv2.flip(image, 1)
        self.displayImage(image, True)

    @QtCore.pyqtSlot()
    def capture_image(self):
        flag, frame = self.cap.read()
        path = r'images/'                         
        if flag:
            QtWidgets.QApplication.beep()
            name = "my_image.jpg"
            cv2.imwrite(os.path.join(path, name), frame)
            self._image_counter += 1
            self.sendRequest()

    def sendRequest(self):
        enc = encryptor.encryptor()
        r = requests.get(url="http://quest.phy.stevens.edu:5050/main?lower=1&higher=422&amount=1")
        startPosition = r.json()['finalrandomarray'][0]
        enc.encrypt_file(startPosition,r'images/'+'my_image.jpg')
        with open(r'images/'+'my_image.jpg.enc', 'rb') as uki:
            img = bytearray(uki.read())
        payload = {'key':startPosition}
        data = json.dumps(payload)
        try:
            result = requests.post('http://quest.phy.stevens.edu:5000/compare_image', data=img, headers={'Content-Type': 'application/octet-stream'})
            result = requests.get('http://quest.phy.stevens.edu:5000/compare_image',json=data, headers = {'content-type': 'application/json'})
            name = result.text.split('.jpg')[0]
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Hello " + name)
            retval = msg.exec_()
            g.setmode(g.BOARD)
            g.setup(31,g.OUT)
            g.output(31,1)
            time.sleep(5)
            g.output(31,0)
            g.cleanup()
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Server down, Try again or later ")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def displayImage(self, img, window=True):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape)==3 :
            if img.shape[2]==4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888
        outImage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window:
            self.image_label.setPixmap(QtGui.QPixmap.fromImage(outImage))

    def startUIWindow(self):
        self.Window = UIWindow()                               # - self
        self.setWindowTitle("UIWindow")

#        self.setCentralWidget(self.Window)
#        self.show()
### +++ vvv
        self.Window.ToolsBTN.clicked.connect(self.goWindow1)

        self.hide()
        self.Window.show()

    def goWindow1(self):
        self.show()
        self.Window.hide()
### +++ ^^^


class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.label = QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.ToolsBTN = QPushButton('text')
#        self.ToolsBTN.move(50, 350)

        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.label)
        self.v_box.addWidget(self.ToolsBTN)
        self.setLayout(self.v_box)


if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    window = video()
    window.setWindowTitle('Image Detection')
    window.setFixedSize(width,height)
    window.show()
    sys.exit(app.exec_())