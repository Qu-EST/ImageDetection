from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.capture = QtWidgets.QPushButton(Form)
        self.capture.setObjectName("capture")
        # self.capture.setGeometry(QtCore.QRect(210, 20, 181, 30))
        self.verticalLayout.addWidget(self.capture)

        #converted start button to the label
        self.control_bt = QtWidgets.QLabel(Form)
        # self.control_bt.setGeometry(QtCore.QRect(210, 50, 181, 16))
        self.control_bt.setObjectName("control_bt")
        self.verticalLayout.addWidget(self.control_bt)

        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        # self.image_label.setGeometry(QtCore.QRect(10, 100, 500, 500))
        self.verticalLayout.addWidget(self.image_label)



        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form",     "Cam view"))
        self.control_bt.setText(_translate("Form", "Stand in the camera and wait for the camera to detect your face. Wait for the response"))
        self.capture.setText(_translate("Form",    "Capture"))