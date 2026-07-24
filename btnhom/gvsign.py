from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

class gvsign(QObject):
    dauhieu2= pyqtSignal()
    def setupUi(self, GVSIGN):
        GVSIGN.setObjectName("GVSIGN")
        GVSIGN.resize(500, 255)
        self.sign_in = QtWidgets.QGroupBox(parent=GVSIGN)
        self.sign_in.setGeometry(QtCore.QRect(0, 0, 500, 255))
        self.sign_in.setObjectName("GVSIGN")
        self.label = QtWidgets.QLabel(parent=self.sign_in)
        self.label.setGeometry(QtCore.QRect(0, 80, 141, 141))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("avt.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.sign_in)
        self.label_2.setGeometry(QtCore.QRect(220, 40, 161, 41))
        self.label_2.setStyleSheet("\n"
"font: 57 24pt \".VnRevue\";")
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.sign_in)
        self.lineEdit.setGeometry(QtCore.QRect(250, 100, 161, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(parent=self.sign_in)
        self.label_3.setGeometry(QtCore.QRect(150, 100, 101, 41))
        font = QtGui.QFont()
        font.setFamily(".VnBlack")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgb(211, 211, 211);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.sign_in)
        self.label_4.setGeometry(QtCore.QRect(150, 170, 101, 41))
        font = QtGui.QFont()
        font.setFamily(".VnBlack")
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgb(211, 211, 211);")
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.sign_in)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 170, 161, 41))
        self.lineEdit_2.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_5 = QtWidgets.QLabel(parent=self.sign_in)
        self.label_5.setGeometry(QtCore.QRect(150, 110, 21, 21))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("pass.svg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.sign_in)
        self.label_6.setGeometry(QtCore.QRect(150, 180, 21, 21))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("email.svg"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.enter=QtWidgets.QPushButton("ENTER",parent=self.sign_in)
        self.enter.setGeometry(QtCore.QRect(200, 213, 160, 40))
        self.enter.clicked.connect(self.kiemtra2)
        self.inra=QtWidgets.QLabel("EMAIL hoặc PASS ko đúng",parent=self.sign_in)
        self.inra.setGeometry(235,13, 200, 40)
        self.inra.setStyleSheet("font-family: Tw Cen MT;color:#F3F3F3")


        self.retranslateUi(GVSIGN)
        QtCore.QMetaObject.connectSlotsByName(GVSIGN)

    def retranslateUi(self, gvsign):
        _translate = QtCore.QCoreApplication.translate
        gvsign.setWindowTitle(_translate("Form", "Form"))
        self.sign_in.setTitle(_translate("Form", "sign_in"))
        self.label_2.setText(_translate("Form", "SIGN-IN"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"center\">  EMAIL GV</p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p align=\"center\">PASS</p></body></html>"))


    def kiemtra2(self):
        if self.lineEdit.text() != "lmao123@gmail.com" or self.lineEdit_2.text() != "lmao123":
            self.inra.setStyleSheet("font-size:10px ;font-family: Tw Cen MT;color:red")
        else:
            self.inra.setText("ĐNhap thành công")
            self.inra.setStyleSheet("font-size:10px ;color:blue")
            self.dauhieu2.emit()

        def change():
            self.inra.setStyleSheet("font-size:10px ;font-family: Tw Cen MT;color:#F3F3F3")
            self.inra.setText("EMAIL hoặc PASS ko đúng")

        QTimer.singleShot(500, change)

def gvmosign():
    GVSIGN = QtWidgets.QWidget()
    ui = gvsign()
    ui.setupUi(GVSIGN)
    GVSIGN.show()
    return GVSIGN,ui