from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject,QTimer
import mysql.connector
class hssign(QObject):
    dauhieu = pyqtSignal()
    def setupUi(self, HSSIGN):
        HSSIGN.setObjectName("HSSIGN")
        HSSIGN.resize(500, 255)
        self.sign_in = QtWidgets.QGroupBox(parent=HSSIGN)
        self.sign_in.setGeometry(QtCore.QRect(0, 0, 500, 255))
        self.sign_in.setObjectName("HSSIGN")
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
        self.label_2.setScaledContents(False)
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
        self.label_5.setPixmap(QtGui.QPixmap("iconavt.svg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.sign_in)
        self.label_6.setGeometry(QtCore.QRect(150, 180, 21, 21))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("iconlock.svg"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.enter=QtWidgets.QPushButton("ENTER",parent=self.sign_in)
        self.enter.setGeometry(QtCore.QRect(200, 213, 160, 40))
        self.enter.clicked.connect(self.kiemtra)
        self.inra = QtWidgets.QLabel(f"Chào mừng {self.lineEdit.text()} đến với thư viện", parent=self.sign_in)
        self.inra.setGeometry(235, 13, 200, 40)
        self.inra.setStyleSheet("font-family: Tw Cen MT;color:#F3F3F3")


        self.retranslateUi(HSSIGN)
        QtCore.QMetaObject.connectSlotsByName(HSSIGN)

    def retranslateUi(self, hssign):
        _translate = QtCore.QCoreApplication.translate
        hssign.setWindowTitle(_translate("Form", "Form"))
        self.sign_in.setTitle(_translate("Form", "sign_in"))
        self.label_2.setText(_translate("Form", "SIGN-IN"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"center\">TEN SV</p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p align=\"center\">MA SV</p></body></html>"))
    #link với sign-in

    def kiemtra(self):
        if self.lineEdit_2.text():
            self.inra.setText(f"Chào mừng {self.lineEdit.text()} đến với thư viện")
            self.inra.setStyleSheet("font-size:10px ;font-family: Tw Cen MT;color:blue")
            self.thread=B(index=[self.lineEdit_2.text(),self.lineEdit.text(),1])
            self.dauhieu.emit()
        else:
            self.inra.setText("Bạn phải nhập mã SV")
            self.inra.setStyleSheet("font-size:10px ;color:red")
        def change():
            self.inra.setStyleSheet("font-size:10px ;color:#F3F3F3")
            self.inra.setText("Bạn phải nhập mã SV")
        QTimer.singleShot(500, change)



def hsmosign():
    HSSIGN = QtWidgets.QWidget()
    ui = hssign()
    ui.setupUi(HSSIGN)
    HSSIGN.show()
    return HSSIGN,ui

#truyen du lieu cho database
class B():
    def __init__(self,index=0):
        super(B,self).__init__()
        a=index
        self.dt = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="332007",
            database="thuvienhs"
        )
        self.mycursor = self.dt.cursor()

        self.mycursor.execute("SELECT MaSV FROM qlyhs")
        b=self.mycursor.fetchall()
        if (a[0],) not in b:
            self.mycursor.execute("INSERT INTO qlyhs (MaSV,TÊNSV,QUANTITY) VALUES (%s,%s,%s)", tuple(a))
            self.dt.commit()
        else:
            self.mycursor.execute("SELECT QUANTITY FROM qlyhs WHERE MaSV = %s",(a[0],))
            a[2]=int(self.mycursor.fetchone()[0])+1
            self.mycursor.execute("DELETE FROM qlyhs WHERE MaSV = %s",(a[0],))
            self.mycursor.execute("INSERT INTO qlyhs (MaSV,TÊNSV,QUANTITY) VALUES (%s,%s,%s)", tuple(a))
            self.dt.commit()
        self.dt.close()

