from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel
def doimaudo():
    nhan.setStyleSheet("font-size:20px;font-family:Arial;font-weight:bold;color:#ff0000;")
    nhan.setFixedWidth(200)
def doimauxanh():
    nhan.setStyleSheet("font-size:20px;font-family:Arial;font-weight:bold;color:violet;")
    nhan.setFixedWidth(200)
app=QApplication([])
destop=QWidget()
destop.resize(400,400)
destop.setWindowTitle("đổi màu")
nhan=QLabel("Dương bị gay",parent=destop)
nhan.setGeometry(150,50,200,200)
nhan.setStyleSheet("font-size:20px;font-family:Arial;font-weight:bold;")
nut1=QPushButton("Màu xanh",parent=destop)
nut1.setGeometry(100,190,60,30)
nut1.setStyleSheet("color:#008000;")
nut2=QPushButton("Màu đỏ",parent=destop)
nut2.setGeometry(250,190,60,30)
nut2.setStyleSheet("color:#ff0000;")
nut1.clicked.connect(doimauxanh)
nut2.clicked.connect(doimaudo)






destop.show()
app.exec()